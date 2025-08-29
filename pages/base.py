"""
Classe base para páginas da aplicação Wave com layout responsivo.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from h2o_wave import Q, ui



class BasePage:
    """
    Página base: gerencia layout, zonas, cards e eventos.
    Integra com sessão via q.client e state_manager.
    """
    def __init__(self, route: str, title: str, app=None, icon: str = 'Page'):
        self.route = route
        self.title = title
        self.icon = icon
        self.cards = {}  # Dict de cards (BaseCard)
        self.app = app  # Referência ao app principal (para state_manager)
        self.handlers = {}  # Handlers de eventos por nome

    def add_card(self, name, card):
        self.cards[name] = card

    def register_handler(self, event_name: str, handler):
        """Registra um handler para um evento específico (ex: botão, form, etc)."""
        self.handlers[event_name] = handler

    def setup_layout(self, q: Q, zones=None):
        """Configura layout simples ou customizado. Adiciona zona de debug se ativo."""
        from core.debug import DebugManager
        from core.debug_layout import add_debug_zone
        # ...implementar layout customizado se necessário...


    async def render(self, q: Q):
        """Renderiza todos os cards da página (ciclo modular)."""
        self.setup_layout(q)
        self.render_cards(q)
        await q.page.save()

    async def handle_events(self, q: Q, state=None, args=None):
        from core.app import WaveApp
        if args is None or not args:
            args = getattr(q.client, 'last_event', {})
        if not isinstance(args, dict):
            args = {}
        for event_name, handler in self.handlers.items():
            if args.get(event_name):
                print(f"[DAZE][PAGE] handler found: {event_name}")
                return await handler(q, state=state, args=args)
        for name, card in self.cards.items():
            card_state = state.get(name) if state and isinstance(state, dict) else None
            print(f"[DAZE][PAGE] propagating to card: {name} (state={card_state})")
            result = await card.handle_events(q, state=card_state, args=args)
            if result:
                print(f"[DAZE][PAGE] event handled by card: {name}")
                return result
        print(f"[DAZE][PAGE] event not handled at page level")
        return None

    def set_state(self, q: Q, key: str, value: Any):
        if self.app and hasattr(self.app, 'state_manager'):
            self.app.state_manager.set_client_state(q, f'{self.route}_{key}', value)

    def get_state(self, q: Q, key: str, default: Any = None):
        if self.app and hasattr(self.app, 'state_manager'):
            return self.app.state_manager.get_client_value(q, f'{self.route}_{key}', default)
        return default
