"""
Classe principal da aplicação Wave - DAZE Template
Versão atualizada para estratégias flexíveis de arquivos estáticos
"""

from typing import Dict, Type, Optional, List
from h2o_wave import main, app, Q, ui, on, run_on
import asyncio
import logging
import sys
import os

# Adicionar o diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.config import get_config
from core.state import StateManager



class WaveApp:
    """Classe principal da aplicação Wave - DAZE Template"""
    def __init__(self, static_strategy: str = "minimal"):
        self.config = get_config()
        self.state_manager = StateManager()
        self.pages: Dict[str, 'BasePage'] = {}
        self.auth_manager: Optional['AuthManager'] = None
        self.static_strategy = static_strategy
        self.static_manager = None
        self.logger = logging.getLogger(__name__)
        self.handlers = {}
        self.debug = False

    def add_page(self, name, page):
        self.pages[name] = page

    def register_handler(self, event_name, handler):
        self.handlers[event_name] = handler

    def set_debug(self, debug):
        self.debug = debug

    @staticmethod
    def get_args(q):
        # Extrai args robustamente e normaliza __kv se presente
        if isinstance(q.args, dict):
            args = q.args
        else:
            try:
                args = dict(q.args)
            except Exception:
                try:
                    args = vars(q.args)
                except Exception:
                    args = {}
        if '__kv' in args and isinstance(args['__kv'], dict) and args['__kv']:
            return args['__kv']
        return args

    def register_wave_event(self, event_name):
        @on(event_name)
        async def handler(q: Q):
            print(f"[DAZE][ON] Evento '{event_name}' recebido via @on")
            args = self.get_args(q)
            if args:
                q.client.last_event = args.copy() if hasattr(args, 'copy') else dict(args)
            await self.handle_events(q, args=args)
            self.render(q)
            await q.page.save()

    async def handle_events(self, q, state=None, args=None):
        if args is None or not args:
            args = getattr(q.client, 'last_event', {})
        if not isinstance(args, dict):
            args = {}
        print(f"[DAZE][APP] handle_events: args={args}")
        for event_name, handler in self.handlers.items():
            if args.get(event_name):
                print(f"[DAZE][APP] handler found: {event_name}")
                return await handler(q, state=state, args=args)
        for name, page in self.pages.items():
            page_state = state.get(name) if state else None
            print(f"[DAZE][APP] propagating to page: {name} (state={page_state})")
            result = await page.handle_events(q, state=page_state, args=args)
            if result:
                print(f"[DAZE][APP] event handled by page: {name}")
                return result
        print(f"[DAZE][APP] event not handled at app level")
        return None

    def render(self, q, state=None):
        for name, page in self.pages.items():
            page.render(q, state=state.get(name) if state else None)

    # --- Exemplo funcional minimalista removido ---
    
    async def _add_stylesheet(self, q: Q, css_url: str) -> None:
        """Adiciona stylesheet à página"""
        try:
            if css_url:
                # Método mais simples para adicionar CSS
                q.page.add_meta(ui.stylesheet(css_url))
                self.logger.info(f"Stylesheet adicionado: {css_url}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar stylesheet: {e}")
    
    async def navigate_to_page(self, q: Q, route: str) -> None:
        """Navega para uma página específica"""
        page = self.get_page(route)
        if not page:
            self.logger.warning(f"Página não encontrada: {route}")
            await self.show_error_page(q, f"Página '{route}' não encontrada")
            return
        
        # Limpar cards anteriores apenas se já há cards rastreados
        try:
            self.state_manager.clear_cards(q, ignore={'meta', 'sidebar', 'header'})
        except Exception as e:
            self.logger.debug(f"Erro ao limpar cards (normal na inicialização): {e}")
        
        # Definir página atual
        self.state_manager.set_client_state(q, 'current_page', route)
        
        # Renderizar página
        try:
            await page.render(q)
            await q.page.save()
        except Exception as e:
            self.logger.error(f"Erro ao renderizar página {route}: {e}")
            await self.show_error_page(q, str(e))
    
    def get_default_route(self) -> str:
        """Retorna rota padrão baseada na primeira página registrada"""
        if self.pages:
            return list(self.pages.keys())[0]
        return '#home'
    
    async def show_error_page(self, q: Q, error_message: str) -> None:
        """Exibe página de erro"""
        q.page['error'] = ui.form_card(
            box='1 1 12 6',
            title='❌ Erro',
            items=[
                ui.text(f"Erro: {error_message}"),
                ui.button('home', label='Voltar ao Início', primary=True)
            ]
        )
        await q.page.save()
