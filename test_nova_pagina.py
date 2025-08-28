"""
Teste da nova página de Relatórios - Demonstração de como adicionar páginas
"""

from h2o_wave import main, app, Q, ui
from core.app import WaveApp

# Importar páginas existentes para comparação
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from pages.base import BasePage
from pages.relatorios import RelatoriosPage

# Página simples para home
class HomePage(BasePage):
    def __init__(self):
        super().__init__(route="home", title="Home")
    
    async def render(self, q: Q):
        self.setup_responsive_layout(q, has_nav=True, has_sidebar=False)
        self.create_responsive_header(q, "🏠 Página Inicial")
        
        nav_items = [
            ui.nav_item(name='home', label='🏠 Home'),
            ui.nav_item(name='relatorios', label='📋 Relatórios'),  # ← Nova página
        ]
        self.create_responsive_nav(q, nav_items)
        
        self.add_card(q, 'home_content', ui.form_card(
            box='content',
            title='Bem-vindo!',
            items=[
                ui.text('**Template DAZE - Sistema de Páginas**'),
                ui.separator(),
                ui.text('Demonstração de como adicionar novas páginas:'),
                ui.text('• ✅ Página Home (atual)'),
                ui.text('• ✅ Página Relatórios (nova)'),
                ui.separator(),
                ui.button('ir_relatorios', label='📋 Ir para Relatórios', primary=True)
            ]
        ))

# Criar aplicação DAZE
daze_app = WaveApp(static_strategy="minimal")

# Criar e registrar páginas
home_page = HomePage()
relatorios_page = RelatoriosPage()  # ← Nova página

# Registrar todas as páginas
daze_app.register_page(home_page)
daze_app.register_page(relatorios_page)  # ← Registrar nova página

@app('/')
async def serve(q: Q):
    """Handler principal demonstrando nova página"""
    
    # Inicialização
    if not hasattr(q.client, 'initialized') or not q.client.initialized:
        await daze_app.init_client(q)
        q.client.initialized = True
        return
    
    # Navegação via nav_card
    if q.args['#nav']:
        nav_value = q.args['#nav']
        if nav_value == 'home':
            await daze_app.navigate_to_page(q, "home")
            return
        elif nav_value == 'relatorios':  # ← Tratar navegação para nova página
            await daze_app.navigate_to_page(q, "relatorios")
            return
    
    # Eventos de botões
    if q.args.ir_relatorios:  # ← Botão direto da home
        await daze_app.navigate_to_page(q, "relatorios")
        return
    
    if q.args.voltar_home:
        await daze_app.navigate_to_page(q, "home")
        return
    
    # Eventos específicos da página de relatórios
    current_page_route = daze_app.state_manager.get_client_value(q, 'current_page', 'home')
    current_page = daze_app.get_page(current_page_route)
    
    if current_page and hasattr(current_page, 'handle_events'):
        if await current_page.handle_events(q):
            await q.page.save()  # Página tratou o evento
            return
    
    # Fallback - re-renderizar página atual
    await daze_app.navigate_to_page(q, current_page_route)

if __name__ == '__main__':
    print("🚀 Iniciando teste da nova página de Relatórios...")
    print("📋 Nova página disponível em: http://localhost:10101")
    print("🔗 Navegue entre Home e Relatórios usando o menu")
    main()
