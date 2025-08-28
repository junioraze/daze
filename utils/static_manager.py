"""
Gerenciador de Arquivos Estáticos para H2O Wave Template

Este módulo fornece uma solução para integração de arquivos estáticos
(CSS, JS, imagens) com o sistema de arquivos virtual do H2O Wave.
"""
import os
import asyncio
from typing import List, Dict, Optional
from h2o_wave import Q


class StaticManager:
    """Gerencia upload e serving de arquivos estáticos para Wave"""
    
    def __init__(self, static_dir: str = "static"):
        self.static_dir = static_dir
        self.uploaded_files: Dict[str, str] = {}
        self._upload_lock = asyncio.Lock()
    
    async def upload_static_files(self, q: Q) -> Dict[str, str]:
        """
        Upload todos os arquivos estáticos para o Wave server
        
        Args:
            q: Query context do Wave
            
        Returns:
            Dict com mapeamento local_path -> wave_url
        """
        async with self._upload_lock:
            if self.uploaded_files:
                return self.uploaded_files
            
            files_to_upload = self._discover_static_files()
            
            if not files_to_upload:
                return {}
            
            try:
                # Upload todos os arquivos de uma vez
                uploaded_paths = await q.site.upload(files_to_upload)
                
                # Criar mapeamento de arquivos locais para URLs do Wave
                for local_path, wave_url in zip(files_to_upload, uploaded_paths):
                    relative_path = os.path.relpath(local_path, self.static_dir)
                    self.uploaded_files[relative_path] = wave_url
                
                print(f"✅ {len(uploaded_paths)} arquivos estáticos enviados para Wave server")
                return self.uploaded_files
                
            except Exception as e:
                print(f"❌ Erro ao enviar arquivos estáticos: {e}")
                return {}
    
    def _discover_static_files(self) -> List[str]:
        """Descobre todos os arquivos estáticos no diretório"""
        static_files = []
        
        if not os.path.exists(self.static_dir):
            print(f"⚠️  Diretório static não encontrado: {self.static_dir}")
            return static_files
        
        # Extensões de arquivos estáticos suportadas
        static_extensions = {'.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf'}
        
        for root, dirs, files in os.walk(self.static_dir):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                
                if ext.lower() in static_extensions:
                    static_files.append(file_path)
        
        return static_files
    
    def get_static_url(self, path: str) -> Optional[str]:
        """
        Obtém a URL do Wave para um arquivo estático
        
        Args:
            path: Caminho relativo do arquivo (ex: 'css/custom.css')
            
        Returns:
            URL do arquivo no Wave server ou None se não encontrado
        """
        return self.uploaded_files.get(path)
    
    def get_css_url(self, filename: str) -> Optional[str]:
        """Conveniência para obter URL de arquivo CSS"""
        css_path = f"css/{filename}"
        return self.get_static_url(css_path)
    
    def get_js_url(self, filename: str) -> Optional[str]:
        """Conveniência para obter URL de arquivo JS"""
        js_path = f"js/{filename}"
        return self.get_static_url(js_path)
    
    def get_image_url(self, filename: str) -> Optional[str]:
        """Conveniência para obter URL de imagem"""
        image_path = f"images/{filename}"
        return self.get_static_url(image_path)
    
    async def upload_directory(self, q: Q, directory_path: str) -> Optional[str]:
        """
        Upload um diretório inteiro preservando estrutura
        
        Args:
            q: Query context
            directory_path: Caminho do diretório para upload
            
        Returns:
            URL base do diretório no Wave server
        """
        if not os.path.exists(directory_path):
            print(f"⚠️  Diretório não encontrado: {directory_path}")
            return None
        
        try:
            # upload_dir retorna uma lista com um item (a URL base do diretório)
            uploaded_dirs = await q.site.upload_dir(directory_path)
            base_url = uploaded_dirs[0] if uploaded_dirs else None
            
            if base_url:
                print(f"✅ Diretório '{directory_path}' enviado para: {base_url}")
            
            return base_url
            
        except Exception as e:
            print(f"❌ Erro ao enviar diretório {directory_path}: {e}")
            return None


# Instância global do gerenciador (singleton pattern)
_static_manager = None

def get_static_manager(static_dir: str = "static") -> StaticManager:
    """Obtém instância singleton do StaticManager"""
    global _static_manager
    if _static_manager is None:
        _static_manager = StaticManager(static_dir)
    return _static_manager


# Funções de conveniência para uso direto
async def upload_static_files(q: Q, static_dir: str = "static") -> Dict[str, str]:
    """Upload arquivos estáticos - função de conveniência"""
    manager = get_static_manager(static_dir)
    return await manager.upload_static_files(q)

def get_static_url(path: str) -> Optional[str]:
    """Obter URL de arquivo estático - função de conveniência"""
    manager = get_static_manager()
    return manager.get_static_url(path)

def get_css_url(filename: str) -> Optional[str]:
    """Obter URL de CSS - função de conveniência"""
    manager = get_static_manager()
    return manager.get_css_url(filename)

def get_js_url(filename: str) -> Optional[str]:
    """Obter URL de JS - função de conveniência"""
    manager = get_static_manager()
    return manager.get_js_url(filename)

def get_image_url(filename: str) -> Optional[str]:
    """Obter URL de imagem - função de conveniência"""
    manager = get_static_manager()
    return manager.get_image_url(filename)
