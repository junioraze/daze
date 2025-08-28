"""
Solução 1: Gerenciador de arquivos estáticos integrado com Wave
Usa diretamente a pasta .venv/www/ do Wave ao invés de duplicar arquivos
"""
import os
import shutil
from pathlib import Path
from typing import Optional, Dict


class WaveStaticManager:
    """Gerencia arquivos estáticos usando diretamente a estrutura do Wave"""
    
    def __init__(self):
        self.venv_path = Path(".venv")
        self.wave_www_path = self.venv_path / "www"
        self.wave_static_path = self.wave_www_path / "wave-static"
        self.custom_static_path = self.wave_www_path / "custom"
        
    def setup_custom_static_dir(self) -> bool:
        """
        Cria diretório para arquivos customizados dentro da estrutura do Wave
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Criar diretório custom dentro de www/
            self.custom_static_path.mkdir(exist_ok=True)
            
            # Criar subdiretórios padrão
            (self.custom_static_path / "css").mkdir(exist_ok=True)
            (self.custom_static_path / "js").mkdir(exist_ok=True)
            (self.custom_static_path / "images").mkdir(exist_ok=True)
            (self.custom_static_path / "fonts").mkdir(exist_ok=True)
            
            print(f"✅ Diretório custom criado: {self.custom_static_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar diretório custom: {e}")
            return False
    
    def add_custom_css(self, css_content: str, filename: str = "custom.css") -> Optional[str]:
        """
        Adiciona CSS customizado diretamente na pasta do Wave
        
        Args:
            css_content: Conteúdo do CSS
            filename: Nome do arquivo CSS
            
        Returns:
            URL relativa do arquivo ou None se erro
        """
        try:
            css_dir = self.custom_static_path / "css"
            css_dir.mkdir(exist_ok=True)
            
            css_file = css_dir / filename
            css_file.write_text(css_content, encoding='utf-8')
            
            # URL relativa que o Wave pode servir
            url = f"/custom/css/{filename}"
            print(f"✅ CSS adicionado: {url}")
            return url
            
        except Exception as e:
            print(f"❌ Erro ao adicionar CSS: {e}")
            return None
    
    def get_custom_url(self, path: str) -> str:
        """
        Gera URL para arquivo customizado
        
        Args:
            path: Caminho relativo (ex: 'css/custom.css')
            
        Returns:
            URL completa para o arquivo
        """
        return f"/custom/{path}"
    
    def copy_assets_to_wave(self, source_dir: str) -> Dict[str, str]:
        """
        Copia arquivos de um diretório fonte para a estrutura do Wave
        
        Args:
            source_dir: Diretório com arquivos a copiar
            
        Returns:
            Mapeamento de arquivos copiados
        """
        copied_files = {}
        
        if not os.path.exists(source_dir):
            print(f"⚠️  Diretório fonte não existe: {source_dir}")
            return copied_files
        
        try:
            # Garantir que custom existe
            self.setup_custom_static_dir()
            
            # Copiar recursivamente
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    source_file = Path(root) / file
                    relative_path = source_file.relative_to(source_dir)
                    dest_file = self.custom_static_path / relative_path
                    
                    # Criar diretório destino se necessário
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copiar arquivo
                    shutil.copy2(source_file, dest_file)
                    
                    # Adicionar ao mapeamento
                    url = f"/custom/{relative_path.as_posix()}"
                    copied_files[str(relative_path)] = url
            
            print(f"✅ {len(copied_files)} arquivos copiados para Wave")
            return copied_files
            
        except Exception as e:
            print(f"❌ Erro ao copiar arquivos: {e}")
            return copied_files


# CSS padrão para o template
DEFAULT_CSS = """
/* DAZE Template - Estilos customizados para H2O Wave */

:root {
    --daze-primary: #2563eb;
    --daze-secondary: #64748b;
    --daze-success: #059669;
    --daze-warning: #d97706;
    --daze-error: #dc2626;
    --daze-bg: #f8fafc;
    --daze-card-bg: #ffffff;
    --daze-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.daze-card {
    background: var(--daze-card-bg);
    border-radius: 8px;
    box-shadow: var(--daze-shadow);
    border: 1px solid #e2e8f0;
}

.daze-header {
    background: linear-gradient(135deg, var(--daze-primary), #3b82f6);
    color: white;
    padding: 1rem;
    border-radius: 8px 8px 0 0;
}

.daze-stat-card {
    text-align: center;
    padding: 1.5rem;
    background: var(--daze-card-bg);
    border-radius: 8px;
    box-shadow: var(--daze-shadow);
    transition: transform 0.2s ease;
}

.daze-stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.15);
}

.daze-button-primary {
    background: var(--daze-primary);
    border-color: var(--daze-primary);
    transition: all 0.2s ease;
}

.daze-button-primary:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
}

.daze-loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid var(--daze-primary);
    border-radius: 50%;
    animation: daze-spin 1s linear infinite;
}

@keyframes daze-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.daze-nav {
    background: var(--daze-card-bg);
    border-bottom: 1px solid #e2e8f0;
    padding: 0.5rem 1rem;
}

.daze-content {
    background: var(--daze-bg);
    min-height: calc(100vh - 60px);
    padding: 1rem;
}

.daze-sidebar {
    background: var(--daze-card-bg);
    border-right: 1px solid #e2e8f0;
    padding: 1rem;
}
"""


def setup_wave_static_integration():
    """Configura integração com sistema de arquivos estáticos do Wave"""
    manager = WaveStaticManager()
    
    # Configurar diretório custom
    if manager.setup_custom_static_dir():
        # Adicionar CSS padrão do DAZE
        css_url = manager.add_custom_css(DEFAULT_CSS, "daze.css")
        
        if css_url:
            print(f"🎨 CSS do DAZE disponível em: {css_url}")
            return manager
    
    return None


if __name__ == "__main__":
    # Testar configuração
    manager = setup_wave_static_integration()
    if manager:
        print("✅ Integração com Wave configurada com sucesso!")
        print(f"📁 Arquivos customizados em: {manager.custom_static_path}")
        print("🔗 URLs base: /custom/[caminho]")
    else:
        print("❌ Falha na configuração")
