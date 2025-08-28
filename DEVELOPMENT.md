# Configuração de Desenvolvimento para Wave Template

## Estrutura do Projeto

A Wave Template está organizada da seguinte forma:

```
wave_template/
├── 📁 core/                 # Núcleo da aplicação
│   ├── app.py              # Classe principal WaveApp
│   ├── config.py           # Configurações centralizadas
│   └── state.py            # Gerenciamento de estado
├── 📁 auth/                 # Sistema de autenticação
│   ├── manager.py          # Gerenciador e provedores
│   └── models.py           # Modelos de usuário
├── 📁 pages/                # Páginas da aplicação
│   ├── base.py             # Classe base para páginas
│   ├── dashboard.py        # Dashboard principal
│   └── analytics.py        # Página de analytics
├── 📁 components/           # Componentes reutilizáveis
│   ├── base.py             # Componente base
│   ├── stats.py            # Componentes de estatísticas
│   ├── charts.py           # Componentes de gráficos
│   └── tables.py           # Componentes de tabelas
├── 📁 services/             # Serviços de negócio
│   ├── data_service.py     # Manipulação de dados
│   └── ai_service.py       # Serviços de IA
├── 📁 utils/                # Utilitários
│   ├── helpers.py          # Funções auxiliares
│   └── validators.py       # Validadores
└── 📁 static/               # Arquivos estáticos
    ├── css/                # Estilos customizados
    └── images/             # Imagens
```

## Desenvolvimento

### 1. Configuração do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração da Aplicação

Edite `core/config.py` ou use variáveis de ambiente:

```python
# Configurações básicas
update_config(
    name="Minha Aplicação",
    description="Descrição da app",
    theme="neon",  # neon, nord, light, dark
    debug=True
)
```

### 3. Criando Nova Página

```python
from pages.base import BasePage
from h2o_wave import ui, Q

class MinhaPage(BasePage):
    def __init__(self, app):
        super().__init__(app, '#minha-pagina', 'Minha Página', 'Icon')
    
    async def render(self, q: Q):
        # Seu código aqui
        self.add_card(q, 'content', ui.form_card(
            box='content',
            items=[
                ui.text_xl('Olá Mundo!')
            ]
        ))

# Registrar a página
app.register_page(MinhaPage(app))
```

### 4. Criando Componente

```python
from components.base import BaseComponent
from h2o_wave import ui

class MeuComponente(BaseComponent):
    def render(self, data=None):
        return ui.form_card(
            box='component',
            items=[
                ui.text(f'Dados: {data}')
            ]
        )
```

### 5. Adicionando Serviço

```python
class MeuServico:
    async def processar_dados(self, dados):
        # Lógica de negócio
        return dados_processados

# Usar no app
servico = MeuServico()
resultado = await servico.processar_dados(dados)
```

## Padrões de Código

### 1. Naming Conventions
- Classes: `PascalCase` (ex: `UserManager`)
- Funções/métodos: `snake_case` (ex: `get_user_data`)
- Constantes: `UPPER_SNAKE_CASE` (ex: `MAX_USERS`)
- Arquivos: `snake_case.py` (ex: `user_manager.py`)

### 2. Estrutura de Métodos em Páginas
```python
async def render(self, q: Q):
    """Método principal de renderização"""
    # 1. Configurar layout se necessário
    # 2. Obter dados
    # 3. Renderizar componentes
    # 4. Adicionar cards
```

### 3. Tratamento de Erros
```python
try:
    resultado = await operacao_perigosa()
    self.show_success(q, "Sucesso!")
except Exception as e:
    self.show_error(q, f"Erro: {str(e)}")
```

### 4. Handlers de Eventos
```python
@on('meu_botao')
async def handle_meu_botao(q: Q):
    """Handler para o botão"""
    # Processar evento
    pass
```

## Debugging

### 1. Logs
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Informação de debug")
logger.info("Informação geral")
logger.warning("Aviso")
logger.error("Erro")
```

### 2. Estado do Cliente
```python
# Verificar estado
print(f"Estado atual: {q.client.app_state}")

# Definir estado
app.state_manager.set_client_state(q, 'chave', 'valor')

# Obter estado
valor = app.state_manager.get_client_value(q, 'chave', 'padrão')
```

### 3. Inspeção de Variáveis
```python
# No handler
print(f"Args recebidos: {q.args}")
print(f"Route atual: {q.route}")
print(f"Cards na página: {list(q.page.keys())}")
```

## Deploy

### 1. Produção
```bash
# Desabilitar debug
export WAVE_DEBUG=false

# Executar
python app.py
```

### 2. Docker (opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 10101

CMD ["python", "app.py"]
```

## Extensões Comuns

### 1. Banco de Dados
```python
# Adicionar ao requirements.txt
# sqlalchemy>=2.0.0
# databases[postgresql]

from sqlalchemy import create_engine
from services.base import BaseService

class DatabaseService(BaseService):
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
```

### 2. APIs Externas
```python
import httpx

class APIService:
    async def fetch_data(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
```

### 3. Cache
```python
from functools import lru_cache

class CacheService:
    @lru_cache(maxsize=128)
    def get_cached_data(self, key):
        # Dados que mudam pouco
        return expensive_operation(key)
```

## Troubleshooting

### Problemas Comuns

1. **Página não carrega**: Verificar se a página foi registrada
2. **Cards não aparecem**: Verificar se `add_card()` foi chamado
3. **Handlers não funcionam**: Verificar decorador `@on()`
4. **Estado perdido**: Verificar se `q.client` está sendo usado
5. **Layout quebrado**: Verificar zonas do layout

### Performance

1. **Evitar**: Muitas chamadas `q.page.save()`
2. **Usar**: Componentes para reutilização
3. **Cache**: Dados que não mudam frequentemente
4. **Lazy loading**: Para dados grandes

## Recursos Úteis

- [Documentação H2O Wave](https://wave.h2o.ai/)
- [Galeria de Componentes](https://wave.h2o.ai/gallery)
- [Exemplos no GitHub](https://github.com/h2oai/wave)
- [Comunidade Discord](https://discord.gg/h2o)
