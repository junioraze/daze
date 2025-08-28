"""
Utilitário de Layout Responsivo para DAZE Template
Centraliza as configurações de layout para todas as aplicações
"""

from typing import Dict, Tuple, List
from h2o_wave import Q, ui


class ResponsiveLayout:
    """Gerenciador de layout responsivo para aplicações DAZE"""
    
    def __init__(self):
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200
        }
        
        # Grid padrão: 12 colunas, altura flexível
        self.grid = {
            'columns': 12,
            'row_height': 'auto'
        }
    
    def get_layout_config(self, device_type: str = 'desktop') -> Dict[str, str]:
        """Retorna configuração de layout baseada no tipo de dispositivo"""
        
        layouts = {
            'mobile': {
                'header': '1 1 12 1',
                'nav': '1 2 12 1',
                'main': '1 3 12 8',
                'sidebar': '1 11 12 3',
                'footer': '1 14 12 1',
                'stats': '1 3 12 2',
                'content_full': '1 3 12 11',
                'content_half': '1 3 12 5',
                'dialog': '2 3 10 8'
            },
            'tablet': {
                'header': '1 1 12 1',
                'nav': '1 2 3 10',
                'main': '4 2 6 8',
                'sidebar': '10 2 3 8',
                'footer': '1 12 12 1',
                'stats': '4 2 9 2',
                'content_full': '4 2 9 10',
                'content_half': '4 2 9 5',
                'dialog': '3 3 8 6'
            },
            'desktop': {
                'header': '1 1 12 1',
                'nav': '1 2 2 10',
                'main': '3 2 7 8',
                'sidebar': '10 2 3 8',
                'footer': '1 12 12 1',
                'stats': '3 2 10 2',
                'content_full': '3 2 10 10',
                'content_half': '3 2 10 5',
                'dialog': '4 3 6 6'
            }
        }
        
        return layouts.get(device_type, layouts['desktop'])
    
    def detect_device_type(self, q: Q) -> str:
        """Detecta tipo de dispositivo baseado em user agent ou viewport"""
        # Implementação básica - em produção, usar q.user.user_agent
        # ou JavaScript para detectar viewport
        
        # Por enquanto, retorna desktop
        # TODO: Implementar detecção real baseada em:
        # - q.user.user_agent
        # - Viewport width via JavaScript
        # - Headers HTTP
        
        return 'desktop'
    
    def create_responsive_grid(self, device_type: str, components: List[Dict]) -> Dict[str, ui.Component]:
        """Cria grid responsivo com componentes"""
        layout = self.get_layout_config(device_type)
        grid_components = {}
        
        for comp in components:
            comp_type = comp.get('type', 'form')
            comp_name = comp.get('name')
            comp_layout = comp.get('layout', 'main')
            comp_props = comp.get('props', {})
            
            box = layout.get(comp_layout, layout['main'])
            
            if comp_type == 'header':
                grid_components[comp_name] = ui.header_card(box=box, **comp_props)
            elif comp_type == 'nav':
                grid_components[comp_name] = ui.nav_card(box=box, **comp_props)
            elif comp_type == 'stats':
                grid_components[comp_name] = ui.stats_card(box=box, **comp_props)
            elif comp_type == 'form':
                grid_components[comp_name] = ui.form_card(box=box, **comp_props)
            elif comp_type == 'chart':
                grid_components[comp_name] = ui.plot_card(box=box, **comp_props)
            
        return grid_components
    
    def get_responsive_columns(self, device_type: str, total_items: int) -> int:
        """Retorna número de colunas ideal baseado no dispositivo e quantidade de itens"""
        column_map = {
            'mobile': min(1, total_items),
            'tablet': min(2, total_items),
            'desktop': min(3, total_items)
        }
        return column_map.get(device_type, 1)
    
    def calculate_card_width(self, device_type: str, columns: int, total_columns: int = 12) -> int:
        """Calcula largura do card baseado no número de colunas"""
        available_columns = total_columns - 1 if device_type != 'mobile' else total_columns
        return max(1, available_columns // columns)
    
    def create_responsive_page_template(self, q: Q, page_config: Dict) -> Dict[str, str]:
        """Cria template de página responsiva baseado na configuração"""
        device_type = self.detect_device_type(q)
        layout = self.get_layout_config(device_type)
        
        # Personalizar layout baseado na configuração da página
        custom_layout = layout.copy()
        
        # Se página não tem sidebar, expandir conteúdo principal
        if not page_config.get('has_sidebar', True):
            if device_type == 'desktop':
                custom_layout['main'] = '3 2 10 8'
            elif device_type == 'tablet':
                custom_layout['main'] = '4 2 9 8'
        
        # Se página não tem navegação, expandir conteúdo
        if not page_config.get('has_nav', True):
            if device_type == 'desktop':
                custom_layout['main'] = '1 2 12 8' if not page_config.get('has_sidebar') else '1 2 9 8'
            elif device_type == 'tablet':
                custom_layout['main'] = '1 2 12 8' if not page_config.get('has_sidebar') else '1 2 9 8'
        
        return custom_layout


# Instância global para uso em toda aplicação
responsive_layout = ResponsiveLayout()


def get_responsive_layout() -> ResponsiveLayout:
    """Retorna instância do gerenciador de layout responsivo"""
    return responsive_layout


def create_responsive_page(q: Q, config: Dict) -> Dict[str, str]:
    """Função utilitária para criar página responsiva"""
    return responsive_layout.create_responsive_page_template(q, config)


def detect_device(q: Q) -> str:
    """Função utilitária para detectar dispositivo"""
    return responsive_layout.detect_device_type(q)
