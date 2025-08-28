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
from utils.layout import get_responsive_layout


class WaveApp:
    """Classe principal da aplicação Wave - DAZE Template"""
    
    def __init__(self, static_strategy: str = "minimal"):
        self.config = get_config()
        self.state_manager = StateManager()
        self.pages: Dict[str, 'BasePage'] = {}
        self.auth_manager: Optional['AuthManager'] = None
        self.static_strategy = static_strategy
        self.static_manager = None
        self.layout_manager = get_responsive_layout()
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging
        if self.config.debug:
            logging.basicConfig(level=logging.DEBUG)
        
        # Inicializar estratégia de arquivos estáticos
        self._init_static_strategy()
        
    def _init_static_strategy(self):
        """Inicializa estratégia de arquivos estáticos"""
        try:
            if self.static_strategy == "wave":
                from utils.wave_static_manager import WaveStaticManager
                self.static_manager = WaveStaticManager()
            elif self.static_strategy == "symlink":
                from utils.symlink_static_manager import SymlinkStaticManager
                self.static_manager = SymlinkStaticManager()
            elif self.static_strategy == "minimal":
                from utils.minimal_static_manager import MinimalStaticManager
                self.static_manager = MinimalStaticManager()
            else:
                raise ValueError(f"Estratégia desconhecida: {self.static_strategy}")
                
            self.logger.info(f"Estratégia de arquivos estáticos: {self.static_strategy}")
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar estratégia estática: {e}")
            # Fallback para minimal
            from utils.minimal_static_manager import MinimalStaticManager
            self.static_manager = MinimalStaticManager()
    
    def register_page(self, page_instance: 'BasePage') -> None:
        """Registra uma página na aplicação"""
        self.pages[page_instance.route] = page_instance
        self.logger.info(f"Página registrada: {page_instance.route}")
    
    def register_auth(self, auth_manager: 'AuthManager') -> None:
        """Registra o gerenciador de autenticação"""
        self.auth_manager = auth_manager
        self.logger.info("Gerenciador de autenticação registrado")
    
    def get_page(self, route: str) -> Optional['BasePage']:
        """Retorna uma página pelo route"""
        return self.pages.get(route)
    
    async def init_client(self, q: Q) -> None:
        """Inicializa o cliente"""
        self.state_manager.initialize_client(q)
        
        # Aplicar tema/estilo baseado na estratégia
        await self._apply_theme(q)
        
        # Verificar autenticação se habilitada
        if self.config.auth_enabled and self.auth_manager:
            if not await self.auth_manager.is_authenticated(q):
                await self.show_login_page(q)
                await q.page.save()
                return
        
        # Carregar página padrão (sem clear_cards na inicialização)
        default_route = self.get_default_route()
        page = self.get_page(default_route)
        if page:
            await page.render(q)
            self.state_manager.set_client_state(q, 'current_page', default_route)
            await q.page.save()
        else:
            self.logger.warning(f"Página padrão não encontrada: {default_route}")
            await self.show_error_page(q, f"Página padrão '{default_route}' não registrada")
            await q.page.save()
    
    async def _apply_theme(self, q: Q) -> None:
        """Aplica tema baseado na estratégia de arquivos estáticos"""
        try:
            if self.static_manager and hasattr(self.static_manager, 'inject_theme_css'):
                # Estratégia minimal - CSS inline
                await self.static_manager.inject_theme_css(q)
                self.logger.info(f"Tema aplicado via estratégia {self.static_strategy}")
            else:
                self.logger.info("Nenhum tema customizado aplicado - usando padrão Wave")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao aplicar tema: {e}")
    
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
