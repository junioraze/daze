"""
Classe base para componentes reutilizáveis.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from h2o_wave import ui


class BaseComponent(ABC):
    """Classe base para todos os componentes"""
    
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__.lower()
        self.config: Dict[str, Any] = {}
    
    @abstractmethod
    def render(self, data: Any = None, **kwargs) -> ui.FormCard:
        """Renderiza o componente"""
        pass
    
    def configure(self, **config) -> 'BaseComponent':
        """Configura o componente"""
        self.config.update(config)
        return self
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Obtém configuração do componente"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Define configuração do componente"""
        self.config[key] = value
    
    def create_loading_card(self, box: str = 'content', message: str = 'Carregando...') -> ui.FormCard:
        """Cria card de carregamento"""
        return ui.form_card(
            box=box,
            items=[
                ui.text('🔄 ' + message),
                ui.progress(label=message)
            ]
        )
    
    def create_error_card(self, box: str = 'content', error: str = 'Erro desconhecido') -> ui.FormCard:
        """Cria card de erro"""
        return ui.form_card(
            box=box,
            items=[
                ui.text('❌ Erro'),
                ui.text(error),
                ui.button(f'retry_{self.name}', 'Tentar Novamente')
            ]
        )
    
    def create_empty_card(self, box: str = 'content', message: str = 'Nenhum dado disponível') -> ui.FormCard:
        """Cria card vazio"""
        return ui.form_card(
            box=box,
            items=[
                ui.text('📭 ' + message)
            ]
        )
