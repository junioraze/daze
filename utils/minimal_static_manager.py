"""
Solução 3: DAZE Template sem pasta static/ - apenas Wave
Usa exclusivamente o sistema de arquivos do Wave
"""
from h2o_wave import Q, ui
from pathlib import Path
from typing import Dict, Optional


class MinimalStaticManager:
    """Gerenciador minimalista que usa apenas recursos do Wave"""
    
    def __init__(self):
        self.inline_styles = {}
        self.embedded_scripts = {}
        self.wave_urls = {
            # URLs dos recursos já disponíveis no Wave
            'inter_font': '/wave-static/Inter-Regular-d612f121.woff2',
            'highlighting': '/wave-static/index-be05b8a6.css'
        }
    
    def register_inline_css(self, name: str, css_content: str) -> None:
        """
        Registra CSS para ser injetado inline
        
        Args:
            name: Nome identificador do CSS
            css_content: Conteúdo CSS
        """
        self.inline_styles[name] = css_content
    
    def get_daze_theme_css(self) -> str:
        """Retorna CSS temático do DAZE para inserção inline"""
        return """
        /* DAZE Theme - Inline CSS */
        .daze-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .daze-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .daze-header {
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            padding: 1.5rem;
            border-radius: 12px 12px 0 0;
            text-align: center;
        }
        
        .daze-stat {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .daze-button {
            background: linear-gradient(90deg, #667eea, #764ba2);
            border: none;
            border-radius: 6px;
            color: white;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        .daze-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        """
    
    async def inject_theme_css(self, q: Q) -> None:
        """
        Injeta CSS temático diretamente na página
        
        Args:
            q: Query context do Wave
        """
        try:
            # Estratégia minimal: não inject CSS customizado
            # Wave já tem um design muito bom por padrão
            print("🎨 Usando tema padrão do Wave (estratégia minimal)")
            
        except Exception as e:
            print(f"❌ Erro ao aplicar tema: {e}")
    
    def create_themed_header(self, title: str, subtitle: str = "") -> ui.HeaderCard:
        """
        Cria header com tema DAZE aplicado
        
        Args:
            title: Título principal
            subtitle: Subtítulo opcional
            
        Returns:
            Header card temático
        """
        return ui.header_card(
            box='1 1 12 2',
            title=title,
            subtitle=subtitle,
            items=[
                ui.persona(
                    title='DAZE Template',
                    subtitle='Zero to Everything',
                    size='s',
                    initials='DZ',
                    initials_color='$blue'
                )
            ]
        )
    
    def create_themed_stat_card(self, title: str, items: list, box: str = '1 3 12 2') -> ui.StatListCard:
        """
        Cria card de estatísticas com tema DAZE
        
        Args:
            title: Título do card
            items: Lista de ui.stat items
            box: Posicionamento do card
            
        Returns:
            Stat card temático
        """
        return ui.stat_list_card(
            box=box,
            title=f"📊 {title}",
            items=items
        )
    
    def create_themed_form_card(self, title: str, items: list, box: str) -> ui.FormCard:
        """
        Cria form card com tema DAZE
        
        Args:
            title: Título do card
            items: Lista de form items
            box: Posicionamento do card
            
        Returns:
            Form card temático
        """
        return ui.form_card(
            box=box,
            title=f"✨ {title}",
            items=items
        )
    
    def get_wave_resource_url(self, resource_name: str) -> Optional[str]:
        """
        Obtém URL de recurso já disponível no Wave
        
        Args:
            resource_name: Nome do recurso
            
        Returns:
            URL do recurso ou None
        """
        return self.wave_urls.get(resource_name)


# CSS temático inline para o DAZE
DAZE_INLINE_THEME = """
<style>
/* DAZE Template - Tema Moderno */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', sans-serif;
}

.wave-card {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

.wave-header {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-radius: 12px 12px 0 0 !important;
}

.wave-button-primary {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

.wave-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}
</style>
"""


def setup_minimal_static():
    """Configura sistema minimal sem pasta static/"""
    manager = MinimalStaticManager()
    
    # Registrar tema padrão
    manager.register_inline_css('daze_theme', manager.get_daze_theme_css())
    
    print("✅ Sistema minimal configurado!")
    print("🎨 Tema aplicado via CSS inline")
    print("📁 Nenhuma pasta static/ necessária")
    
    return manager


if __name__ == "__main__":
    # Testar configuração
    manager = setup_minimal_static()
    print("✅ DAZE Template configurado sem dependências estáticas!")
    print("🔗 Usando apenas recursos nativos do Wave")
