"""
DAZE Template - Header Component
Header de navegação que consulta páginas registradas no app
"""

from h2o_wave import Q, ui
from .base import BaseComponent


class HeaderComponent(BaseComponent):
    """
    Componente de header que consulta páginas registradas no app principal.
    Não é uma página - é um componente que vai dentro de cards.
    """
    
    def __init__(self, component_id: str = 'header', app=None):
        super().__init__(component_id)
        self.app = app  # Referência ao app para consultar páginas registradas
    
    def create(self, q: Q, **kwargs):
        """Cria o header com navegação dinâmica baseada nas páginas do app"""
        nav_items = self._get_navigation_items()
        current_page = kwargs.get('current_page', 'dashboard')
        
        q.page[self.component_id] = ui.nav_card(
            box='header',
            title='🌊 DAZE - H2O Wave Template',
            subtitle=self._get_page_description(current_page),
            items=nav_items,
            value=current_page
        )
    
    def update(self, q: Q, **kwargs):
        """Atualiza o header (re-cria para manter sincronizado)"""
        self.create(q, **kwargs)
    
    def _get_navigation_items(self):
        """Consulta páginas registradas no app principal"""
        if not self.app or not hasattr(self.app, 'pages'):
            # Fallback se não há app ou páginas registradas
            return [ui.nav_item(name='dashboard', label='📊 Dashboard')]
        
        nav_items = []
        for route, page in self.app.pages.items():
            nav_items.append(
                ui.nav_item(
                    name=route,
                    label=f'{getattr(page, "icon", "📄")} {page.title}'
                )
            )
        
        return nav_items
    
    def _get_page_description(self, current_page):
        """Retorna descrição da página atual"""
        if not self.app or not hasattr(self.app, 'pages'):
            return 'Template modular para H2O Wave'
        
        page = self.app.pages.get(current_page)
        if page and hasattr(page, 'description'):
            return page.description
        
        return f'Página: {current_page}'


class BreadcrumbComponent(BaseComponent):
    """Componente de breadcrumb para navegação contextual"""
    
    def __init__(self, component_id: str = "breadcrumb"):
        super().__init__(component_id)
    
    def create(self, q: Q, **kwargs):
        """Cria o breadcrumb"""
        current_page = kwargs.get('current_page', 'dashboard')
        filters = kwargs.get('applied_filters', {})
        
        # Monta texto do breadcrumb
        breadcrumb_text = f'🏠 **DAZE** > **{current_page.title()}**'
        
        # Adiciona filtros aplicados se houver
        if filters:
            filter_text = ', '.join([f'{k}: {v}' for k, v in filters.items()])
            breadcrumb_text += f' > _Filtros: {filter_text}_'
        
        q.page[self.component_id] = ui.form_card(
            box='breadcrumb',
            items=[ui.text_m(breadcrumb_text)]
        )
    
    def update(self, q: Q, **kwargs):
        """Atualiza o breadcrumb"""
        self.create(q, **kwargs)
