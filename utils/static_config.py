"""
Configuração alternativa para servir arquivos estáticos diretamente via Wave server

Este arquivo demonstra como configurar o Wave server para servir arquivos estáticos
diretamente do filesystem, sem precisar fazer upload via q.site.upload().
"""

# Para usar este método, inicie o Wave server com os seguintes parâmetros:

WAVE_SERVER_CONFIG = {
    "public_dir": "/static/@./wave_template/static",
    "private_dir": "/assets/@./wave_template/static", 
}

# Comandos para iniciar o Wave server:

# Opção 1: Via linha de comando
CMD_PUBLIC_DIR = 'waved -public-dir "/static/@./wave_template/static"'

# Opção 2: Via variável de ambiente  
ENV_PUBLIC_DIR = 'H2O_WAVE_PUBLIC_DIR="/static/@./wave_template/static"'

# Opção 3: Via arquivo .env
ENV_FILE_CONFIG = """
# Configuração do Wave Server para arquivos estáticos
H2O_WAVE_PUBLIC_DIR="/static/@./wave_template/static"
H2O_WAVE_PRIVATE_DIR="/assets/@./wave_template/static"
"""

# URLs resultantes:
# Arquivo: ./wave_template/static/css/custom.css
# URL: http://localhost:10101/static/css/custom.css

# Arquivo: ./wave_template/static/images/logo.png  
# URL: http://localhost:10101/static/images/logo.png


def get_static_url_direct(filename: str, subdir: str = "") -> str:
    """
    Gera URL para arquivo estático quando usando método direto
    
    Args:
        filename: Nome do arquivo (ex: 'custom.css')
        subdir: Subdiretório (ex: 'css', 'js', 'images')
        
    Returns:
        URL completa para o arquivo
    """
    if subdir:
        return f"/static/{subdir}/{filename}"
    return f"/static/{filename}"

def get_css_url_direct(filename: str) -> str:
    """URL para arquivo CSS via método direto"""
    return get_static_url_direct(filename, "css")

def get_js_url_direct(filename: str) -> str:
    """URL para arquivo JS via método direto"""
    return get_static_url_direct(filename, "js")

def get_image_url_direct(filename: str) -> str:
    """URL para imagem via método direto"""
    return get_static_url_direct(filename, "images")


# Configuração para wave run com arquivos estáticos
WAVE_RUN_COMMAND = """
# Para usar com wave run, crie um arquivo .env:
cat > .env << EOF
H2O_WAVE_PUBLIC_DIR="/static/@./wave_template/static"
EOF

# Então execute:
wave run app.py
"""

print(f"""
🌊 CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS PARA H2O WAVE

Método 1 - Via Upload (Recomendado):
- Use utils/static_manager.py
- Arquivos são enviados automaticamente para Wave server
- Funciona em qualquer ambiente

Método 2 - Via Configuração Direta:
- Configure Wave server com: {CMD_PUBLIC_DIR}
- Ou use variável de ambiente: {ENV_PUBLIC_DIR}
- Serve arquivos diretamente do filesystem

URLs de exemplo:
- CSS: {get_css_url_direct('custom.css')}
- JS: {get_js_url_direct('app.js')}
- Imagem: {get_image_url_direct('logo.png')}
""")
