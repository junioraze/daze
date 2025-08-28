"""
Gerenciamento de estado centralizado para aplicações Wave.
"""

from typing import Any, Dict, Optional, Set
from h2o_wave import Q
import asyncio


class StateManager:
    """Gerenciador de estado da aplicação"""
    
    def __init__(self):
        self._global_state: Dict[str, Any] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
    
    def get_client_state(self, q: Q) -> Dict[str, Any]:
        """Retorna o estado do cliente"""
        if not hasattr(q.client, 'app_state') or q.client.app_state is None:
            q.client.app_state = {}
        return q.client.app_state
    
    def set_client_state(self, q: Q, key: str, value: Any) -> None:
        """Define um valor no estado do cliente"""
        state = self.get_client_state(q)
        if state is not None:
            state[key] = value
        else:
            # Fallback de segurança
            q.client.app_state = {key: value}
    
    def get_client_value(self, q: Q, key: str, default: Any = None) -> Any:
        """Obtém um valor do estado do cliente"""
        state = self.get_client_state(q)
        return state.get(key, default)
    
    def clear_client_state(self, q: Q) -> None:
        """Limpa o estado do cliente"""
        if hasattr(q.client, 'app_state'):
            q.client.app_state.clear()
    
    async def set_global_state(self, key: str, value: Any) -> None:
        """Define um valor no estado global com lock"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        
        async with self._locks[key]:
            self._global_state[key] = value
    
    async def get_global_state(self, key: str, default: Any = None) -> Any:
        """Obtém um valor do estado global com lock"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        
        async with self._locks[key]:
            return self._global_state.get(key, default)
    
    def get_tracked_cards(self, q: Q) -> Set[str]:
        """Retorna o conjunto de cards rastreados"""
        if not hasattr(q.client, 'tracked_cards'):
            q.client.tracked_cards = set()
        return q.client.tracked_cards
    
    def add_card(self, q: Q, name: str) -> None:
        """Adiciona um card ao conjunto rastreado"""
        cards = self.get_tracked_cards(q)
        cards.add(name)
    
    def remove_card(self, q: Q, name: str) -> None:
        """Remove um card do conjunto rastreado"""
        cards = self.get_tracked_cards(q)
        cards.discard(name)
        if name in q.page:
            del q.page[name]
    
    def clear_cards(self, q: Q, ignore: Optional[Set[str]] = None) -> None:
        """Remove todos os cards rastreados, exceto os ignorados"""
        if ignore is None:
            ignore = set()
        
        cards = self.get_tracked_cards(q)
        if cards is not None:
            cards_to_remove = cards - ignore
            
            for card_name in cards_to_remove:
                if card_name in q.page:
                    del q.page[card_name]
            
            # Atualiza o conjunto de cards rastreados
            cards.clear()
        cards.update(ignore)
    
    def initialize_client(self, q: Q) -> None:
        """Inicializa o estado do cliente"""
        if not hasattr(q.client, 'initialized'):
            q.client.initialized = True
            q.client.app_state = {}
            q.client.tracked_cards = set()
            q.client.current_page = None
