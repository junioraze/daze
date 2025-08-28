"""
Classe base para páginas da aplicação Wave com layout responsivo.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from h2o_wave import Q, ui


class BasePage(ABC):
    """Classe base para todas as páginas da aplicação com layout responsivo"""
    
    def __init__(self, route: str, title: str, description: str = "", icon: str = 'Page'):
        self.route = route
        self.title = title
        self.description = description
        self.icon = icon
        self.show_in_nav = True
        
    def setup_responsive_layout(self, q: Q, has_nav: bool = True, has_sidebar: bool = False) -> None:
        """Configura layout responsivo usando meta_card com zonas"""
        
        # Limpar qualquer meta_card existente primeiro
        try:
            if q.page['meta']:
                del q.page['meta']
        except:
            pass  # Se não existir, ignoramos
        
        # Layout para mobile (xs - até 768px) - sempre stack vertical
        mobile_zones = [
            ui.zone('header', size='60px'),
            ui.zone('content', size='1fr'),
            ui.zone('footer', size='40px'),
        ]
        
        # Layout para desktop (m - acima de 768px)
        if has_nav and has_sidebar:
            # Layout completo: nav + content + sidebar
            desktop_zones = [
                ui.zone('header', size='60px'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('nav', size='200px'),
                    ui.zone('content', size='1fr'),
                    ui.zone('sidebar', size='250px'),
                ]),
                ui.zone('footer', size='40px'),
            ]
        elif has_nav:
            # Layout com navegação apenas
            desktop_zones = [
                ui.zone('header', size='60px'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('nav', size='200px'),
                    ui.zone('content', size='1fr'),
                ]),
                ui.zone('footer', size='40px'),
            ]
        elif has_sidebar:
            # Layout com sidebar apenas
            desktop_zones = [
                ui.zone('header', size='60px'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('content', size='1fr'),
                    ui.zone('sidebar', size='250px'),
                ]),
                ui.zone('footer', size='40px'),
            ]
        else:
            # Layout simples - apenas content
            desktop_zones = [
                ui.zone('header', size='60px'),
                ui.zone('content', size='1fr'),
                ui.zone('footer', size='40px'),
            ]
        
        # Configurar meta_card com layouts responsivos
        try:
            q.page['meta'] = ui.meta_card(
                box='',
                layouts=[
                    ui.layout(
                        breakpoint='xs',
                        zones=mobile_zones
                    ),
                    ui.layout(
                        breakpoint='m',
                        zones=desktop_zones
                    )
                ]
            )
        except Exception as e:
            # Fallback para layout simples se houver erro
            q.page['meta'] = ui.meta_card(
                box='',
                layouts=[
                    ui.layout(
                        breakpoint='xs',
                        zones=[
                            ui.zone('header', size='60px'),
                            ui.zone('content', size='1fr'),
                        ]
                    )
                ]
            )
    
    @abstractmethod
    async def render(self, q: Q) -> None:
        """Renderiza a página"""
        pass
    
    def add_card(self, q: Q, name: str, card) -> None:
        """Adiciona um card à página"""
        q.page[name] = card
    
    def create_responsive_header(self, q: Q, subtitle: str = None) -> None:
        """Cria header responsivo padrão"""
        self.add_card(q, 'header', ui.header_card(
            box='header',  # Usar zona definida no meta_card
            title=f'{self.icon} {self.title}',
            subtitle=subtitle or self.description,
            image='https://wave.h2o.ai/img/h2o-logo.svg'
        ))
    
    def create_responsive_nav(self, q: Q, items: List[ui.NavItem]) -> None:
        """Cria navegação responsiva usando NavGroup"""
        # NavCard precisa de NavGroup, não NavItem diretamente
        nav_group = ui.nav_group(label='Menu', items=items)
        
        self.add_card(q, 'nav', ui.nav_card(
            box='nav',  # Usar zona definida no meta_card
            items=[nav_group]
        ))
    
    def create_responsive_stats(self, q: Q, stats: List[ui.Stat], title: str = None) -> None:
        """Cria estatísticas responsivas na zona content usando form_card"""
        
        # Converter stats para itens de form
        items = []
        if title:
            items.append(ui.text(f'**{title}**'))
            items.append(ui.separator())
        
        for i, stat in enumerate(stats):
            items.append(ui.text(f'**{stat.label}:** {stat.value} {stat.icon if stat.icon else ""}'))
        
        self.add_card(q, 'stats', ui.form_card(
            box='content',  # Usar zona definida no meta_card
            items=items
        ))
    
    def get_main_box(self, q: Q, has_sidebar: bool = False) -> str:
        """Retorna zona de conteúdo principal"""
        return 'content'  # Sempre usar a zona content definida no layout
    
    def get_sidebar_box(self, q: Q) -> str:
        """Retorna zona de sidebar"""
        return 'sidebar'  # Sempre usar a zona sidebar definida no layout
    
    def create_responsive_footer(self, q: Q, content: List[ui.Component]) -> None:
        """Cria footer responsivo"""
        self.add_card(q, 'footer', ui.form_card(
            box='footer',  # Usar zona footer
            items=content
        ))
    
    def set_title(self, q: Q, title: str = None) -> None:
        """Define o título da página"""
        page_title = title or self.title
        q.page['title'] = ui.form_card(
            box='',
            items=[ui.text(f'# {page_title}')]
        )
        """Define um valor no estado da página"""
        self.app.state_manager.set_client_state(q, f'{self.route}_{key}', value)
    
    def get_state(self, q: Q, key: str, default: Any = None) -> Any:
        """Obtém um valor do estado da página"""
        return self.app.state_manager.get_client_value(q, f'{self.route}_{key}', default)
    
    async def on_navigate_to(self, q: Q) -> None:
        """Chamado quando a página é navegada"""
        pass
    
    async def on_navigate_from(self, q: Q) -> None:
        """Chamado quando saindo da página"""
        pass
    
    def create_breadcrumb(self) -> List[ui.Component]:
        """Cria breadcrumb para a página"""
        return [
            ui.breadcrumb(name='home', label='Home'),
            ui.breadcrumb(name=self.route, label=self.title)
        ]
    
    def create_page_header(self, subtitle: str = "") -> ui.FormCard:
        """Cria cabeçalho padrão da página"""
        items = [
            ui.breadcrumbs(items=self.create_breadcrumb()),
            ui.text_xl(f'{self.icon} {self.title}')
        ]
        
        if subtitle:
            items.append(ui.text_l(subtitle))
        
        return ui.form_card(
            box='page_header',
            items=items
        )
    
    def show_loading(self, q: Q, message: str = "Carregando...") -> None:
        """Exibe indicador de carregamento"""
        self.add_card(q, 'loading', ui.form_card(
            box='content',
            items=[
                ui.text_xl('🔄 ' + message),
                ui.progress(label=message)
            ]
        ))
    
    def hide_loading(self, q: Q) -> None:
        """Remove indicador de carregamento"""
        self.remove_card(q, 'loading')
    
    def show_error(self, q: Q, error: str) -> None:
        """Exibe mensagem de erro"""
        self.add_card(q, 'error', ui.form_card(
            box='content',
            items=[
                ui.text_xl('❌ Erro'),
                ui.text(error),
                ui.button('retry', 'Tentar Novamente', primary=True)
            ]
        ))
    
    def show_success(self, q: Q, message: str) -> None:
        """Exibe mensagem de sucesso"""
        self.add_card(q, 'success', ui.form_card(
            box='content',
            items=[
                ui.message_bar(type='success', text=message)
            ]
        ))
