"""
DAZE Template - Base Components
Arquitetura modular para H2O Wave applications

Classes fundamentais:
- BaseComponent: Para componentes reutilizáveis (charts, stats, tables)
- BaseCard: Para containers que orquestram múltiplos componentes
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

# Import h2o_wave only when available
try:
    from h2o_wave import main, app, Q, ui
except ImportError:
    # For syntax checking without h2o_wave installed
    Q = Any



class BaseComponent:
    """
    Componente DAZE modular: handlers, renderização, estado e eventos.
    """
    def __init__(self, component_id):
        self.component_id = component_id
        self.handlers = {}

    def register_handler(self, event_name, handler):
        self.handlers[event_name] = handler

    def render(self, q, state=None):
        raise NotImplementedError

    async def handle_events(self, q, state=None, args=None, **kwargs):
        # Fallback robusto de evento/args
        if args is None or not args:
            args = getattr(q.client, 'last_event', {})
        if not isinstance(args, dict):
            args = {}
        # Dispatch automático: procura métodos on_<evento>
        for event_name in args:
            method = getattr(self, f'on_{event_name}', None)
            if callable(method):
                print(f"[DAZE][COMPONENT] dispatch automático: on_{event_name}")
                result = await method(q, state=state, args=args) if hasattr(method, '__await__') else method(q, state=state, args=args)
                # Salva resultado padronizado
                if not hasattr(q.client, 'result') or not isinstance(getattr(q.client, 'result', None), dict):
                    q.client.result = {}
                q.client.result[event_name] = result
                return True
        # Fallback: handlers registrados manualmente
        for event_name, handler in self.handlers.items():
            if args.get(event_name):
                print(f"[DAZE][COMPONENT] handler found: {event_name}")
                return await handler(q, state=state, args=args)
        print(f"[DAZE][COMPONENT] event not handled at component level")
        return None

    def get_result(self, q, event_name):
        result = getattr(q.client, 'result', None)
        if not result or not isinstance(result, dict):
            return None
        return result.get(event_name)



class BaseCard:
    """
    Card DAZE modular: orquestra componentes, handlers, estado e eventos.
    """
    def __init__(self, card_id):
        self.card_id = card_id
        self.components = {}
        self.handlers = {}

    def add_component(self, name, component):
        self.components[name] = component

    def register_handler(self, event_name, handler):
        self.handlers[event_name] = handler

    def set_zone(self, zone):
        self.zone = zone

    def render(self, q, zone=None, state=None, **kwargs):
        for name, component in self.components.items():
            component.render(q, state=state.get(name) if state else None)

    async def handle_events(self, q, state=None, args=None, **kwargs):
        from core.app import WaveApp
        if args is None or not args:
            args = getattr(q.client, 'last_event', {})
        if not isinstance(args, dict):
            args = {}
        print(f"[DAZE][CARD] {self.card_id} handle_events: args={args}")
        for event_name, handler in self.handlers.items():
            if args.get(event_name):
                print(f"[DAZE][CARD] handler found: {event_name}")
                return await handler(q, state=state, args=args)
        for name, component in self.components.items():
            comp_state = state.get(name) if state and isinstance(state, dict) else None
            print(f"[DAZE][CARD] propagating to component: {name} (state={comp_state})")
            result = await component.handle_events(q, state=comp_state, args=args)
            if result:
                print(f"[DAZE][CARD] event handled by component: {name}")
                return result
        print(f"[DAZE][CARD] event not handled at card level")
        return None
