"""
Solução 2: Usar symlink para conectar template static/ com Wave www/
Evita duplicação mantendo estrutura familiar do template
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, List


class SymlinkStaticManager:
    """Gerencia arquivos estáticos usando symlinks com Wave"""
    
    def __init__(self):
        self.template_static = Path("static")
        self.wave_www = Path(".venv/www")
        self.wave_custom = self.wave_www / "daze-static"
        
    def create_symlink_integration(self) -> bool:
        """
        Cria symlink entre static/ do template e www/ do Wave
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # Verificar se diretório Wave existe
            if not self.wave_www.exists():
                print("❌ Diretório .venv/www não encontrado")
                return False
            
            # Remover symlink existente se houver
            if self.wave_custom.exists() or self.wave_custom.is_symlink():
                if self.wave_custom.is_symlink():
                    self.wave_custom.unlink()
                else:
                    import shutil
                    shutil.rmtree(self.wave_custom)
            
            # Criar symlink do static/ para www/daze-static/
            if os.name == 'nt':  # Windows
                self._create_windows_symlink()
            else:  # Unix/Linux/macOS
                self._create_unix_symlink()
            
            print(f"✅ Symlink criado: {self.template_static} -> {self.wave_custom}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar symlink: {e}")
            return False
    
    def _create_windows_symlink(self):
        """Cria symlink no Windows"""
        cmd = [
            'mklink', '/D', 
            str(self.wave_custom.absolute()), 
            str(self.template_static.absolute())
        ]
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Falha ao criar symlink: {result.stderr}")
    
    def _create_unix_symlink(self):
        """Cria symlink no Unix/Linux/macOS"""
        self.wave_custom.symlink_to(self.template_static.absolute())
    
    def get_static_url(self, path: str) -> str:
        """
        Gera URL para arquivo estático via symlink
        
        Args:
            path: Caminho relativo (ex: 'css/custom.css')
            
        Returns:
            URL para o arquivo
        """
        return f"/daze-static/{path}"
    
    def list_available_files(self) -> Dict[str, str]:
        """
        Lista arquivos disponíveis via symlink
        
        Returns:
            Mapeamento arquivo -> URL
        """
        files_map = {}
        
        if not self.template_static.exists():
            return files_map
        
        for file_path in self.template_static.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.template_static)
                url = self.get_static_url(str(relative_path).replace('\\', '/'))
                files_map[str(relative_path)] = url
        
        return files_map
    
    def validate_symlink(self) -> bool:
        """
        Valida se o symlink está funcionando corretamente
        
        Returns:
            True se válido, False caso contrário
        """
        try:
            # Verificar se symlink existe
            if not self.wave_custom.exists():
                return False
            
            # Verificar se é realmente um symlink
            if not self.wave_custom.is_symlink():
                return False
            
            # Verificar se aponta para o local correto
            target = self.wave_custom.resolve()
            expected = self.template_static.resolve()
            
            return target == expected
            
        except Exception:
            return False


def setup_symlink_static():
    """Configura sistema de arquivos estáticos via symlink"""
    manager = SymlinkStaticManager()
    
    # Criar symlink
    if manager.create_symlink_integration():
        # Validar configuração
        if manager.validate_symlink():
            files = manager.list_available_files()
            print(f"✅ {len(files)} arquivos disponíveis via symlink")
            return manager
        else:
            print("❌ Validação do symlink falhou")
    
    return None


if __name__ == "__main__":
    # Testar configuração
    manager = setup_symlink_static()
    if manager:
        print("✅ Sistema symlink configurado!")
        files = manager.list_available_files()
        print("📁 Arquivos disponíveis:")
        for file, url in files.items():
            print(f"  {file} -> {url}")
    else:
        print("❌ Falha na configuração do symlink")
