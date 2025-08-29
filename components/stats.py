"""
Componente de estatísticas reutilizável.
"""

from typing import List, Dict, Any
from h2o_wave import ui

from .base import BaseComponent


class StatsComponent(BaseComponent):
    """Componente para exibir estatísticas em cards"""
    
    def __init__(self, component_id: str):
        super().__init__(component_id)
    
    def create(self, q, stats_data: List[Dict[str, Any]] = None, 
               box: str = 'content', title: str = 'Estatísticas', **kwargs):
        """Cria o componente de estatísticas na página Wave"""
        if not stats_data:
            stats_data = [{'label': 'Sem dados', 'value': '0', 'icon': 'Info'}]
        
        # Converter dados para ui.stat items
        stat_items = []
        for stat in stats_data:
            stat_items.append(ui.stat(
                label=stat.get('label', 'Label'),
                value=str(stat.get('value', '0')),
                icon=stat.get('icon', 'Info')
            ))
        
        q.page[self.component_id] = ui.form_card(
            box=box,
            title=title,
            items=[ui.stats(items=stat_items)]
        )
    
    def update(self, q, **kwargs):
        """Atualiza as estatísticas com novos dados"""
        # Re-criar com os novos dados
        self.create(q, **kwargs)
    
    def render(self, data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza o componente de estatísticas
        
        Args:
            data: Lista de dicionários com as estatísticas
                Formato: {
                    'label': str,
                    'value': str,
                    'icon': str,
                    'change': float (opcional),
                    'trend': str (opcional: 'up' ou 'down')
                }
        """
        box = kwargs.get('box', 'stats')
        
        if not data:
            return self.create_empty_card(box, 'Nenhuma estatística disponível')
        
        # Criar itens de estatística
        stat_items = []
        for stat in data:
            # Determinar cor do ícone baseado na tendência
            icon_color = None
            if stat.get('trend'):
                icon_color = '#00ff00' if stat['trend'] == 'up' else '#ff4444'
            
            # Criar texto de mudança se disponível
            change_text = None
            if 'change' in stat:
                change_symbol = '↗️' if stat.get('trend') == 'up' else '↘️'
                change_text = f"{change_symbol} {stat['change']:+.1f}%"
            
            stat_item = ui.stat(
                label=stat['label'],
                value=stat['value'],
                icon=stat.get('icon', 'Info'),
                icon_color=icon_color
            )
            
            stat_items.append(stat_item)
        
        return ui.stats_card(
            box=box,
            items=stat_items
        )
    
    def render_single_stat(self, label: str, value: str, icon: str = 'Info', 
                          change: float = None, trend: str = None, **kwargs) -> ui.FormCard:
        """Renderiza uma única estatística"""
        data = [{
            'label': label,
            'value': value,
            'icon': icon,
            'change': change,
            'trend': trend
        }]
        return self.render(data, **kwargs)
    
    def render_grid_stats(self, data: List[Dict[str, Any]], columns: int = 2, **kwargs) -> ui.FormCard:
        """Renderiza estatísticas em grid"""
        box = kwargs.get('box', 'stats')
        
        if not data:
            return self.create_empty_card(box, 'Nenhuma estatística disponível')
        
        # Dividir dados em grupos baseado no número de colunas
        groups = [data[i:i + columns] for i in range(0, len(data), columns)]
        
        items = []
        for group in groups:
            row_items = []
            for stat in group:
                icon_color = None
                if stat.get('trend'):
                    icon_color = '#00ff00' if stat['trend'] == 'up' else '#ff4444'
                
                row_items.append(
                    ui.stat(
                        label=stat['label'],
                        value=stat['value'],
                        icon=stat.get('icon', 'Info'),
                        icon_color=icon_color
                    )
                )
            
            items.append(ui.stats(items=row_items, justify='between'))
        
        return ui.form_card(
            box=box,
            items=items
        )
