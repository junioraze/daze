"""
Configurações centralizadas da aplicação Wave.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os


@dataclass
class AppConfig:
    """Configurações da aplicação"""
    
    # Informações básicas
    name: str = "DAZE App"
    version: str = "1.0.0"
    description: str = "DAZE Template - H2O Wave"
    
    # Configurações de UI
    theme: str = "minimal"  # minimal, neon, nord, light, dark
    static_strategy: str = "minimal"  # minimal, wave, symlink
    title: str = "Wave Application"
    
    # Configurações de autenticação
    auth_enabled: bool = True
    auth_type: str = "simple"  # simple, oauth, ldap
    
    # Configurações do servidor
    host: str = "localhost"
    port: int = 10101
    debug: bool = False
    
    # Configurações de layout
    default_layout: str = "default"
    sidebar_width: str = "250px"
    header_height: str = "80px"
    
    # Configurações de dados
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    temp_dir: str = "temp"
    
    # Configurações customizadas
    custom_settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_settings is None:
            self.custom_settings = {}


# Instância global de configuração
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Retorna a instância global de configuração"""
    global _config
    if _config is None:
        _config = AppConfig()
        
        # Carregar configurações de variáveis de ambiente
        _config.name = os.getenv("WAVE_APP_NAME", _config.name)
        _config.theme = os.getenv("WAVE_THEME", _config.theme)
        _config.debug = os.getenv("WAVE_DEBUG", "false").lower() == "true"
        _config.auth_enabled = os.getenv("WAVE_AUTH_ENABLED", "true").lower() == "true"
        
    return _config


def update_config(**kwargs) -> None:
    """Atualiza configurações da aplicação"""
    global _config
    config = get_config()
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            config.custom_settings[key] = value
