# 🌊 H2O Wave Modular Template

## 📋 Sobre

Esta template foi desenvolvida para criar aplicações H2O Wave modernas, escaláveis e bem estruturadas. Ela resolve os problemas comuns de:
- **Aplicações monolíticas** em um único arquivo
- **Alto acoplamento** entre componentes
- **Baixa manutenibilidade** do código
- **Dificuldade de reutilização** de componentes

## 🏗️ Arquitetura

A template segue uma arquitetura em camadas inspirada em padrões de design modernos:

```
wave_template/
├── app.py                 # Ponto de entrada principal
├── core/                  # Core da aplicação
│   ├── __init__.py
│   ├── app.py            # Classe principal da aplicação
│   ├── config.py         # Configurações centralizadas
│   └── state.py          # Gerenciamento de estado
├── auth/                  # Sistema de autenticação
│   ├── __init__.py
│   ├── manager.py        # Gerenciador de autenticação
│   └── models.py         # Modelos de usuário
├── pages/                 # Páginas/Views da aplicação
│   ├── __init__.py
│   ├── base.py           # Classe base para páginas
│   ├── login.py          # Página de login
│   └── dashboard.py      # Página principal
├── components/            # Componentes reutilizáveis
│   ├── __init__.py
│   ├── base.py           # Componente base
│   ├── forms.py          # Formulários
│   ├── charts.py         # Gráficos
│   └── tables.py         # Tabelas
├── services/              # Serviços/Business Logic
│   ├── __init__.py
│   ├── data_service.py   # Serviços de dados
│   └── ai_service.py     # Serviços de IA
├── utils/                 # Utilitários
│   ├── __init__.py
│   ├── helpers.py        # Funções auxiliares
│   └── validators.py     # Validadores
├── static/                # Arquivos estáticos
│   ├── css/
│   ├── images/
│   └── js/
└── requirements.txt       # Dependências
```

## 🎯 Por que Esta Arquitetura Resolve Seus Problemas

### 1. **Elimina Monolitismo** 
Seus apps atuais (`app.py`, `cockpit.py`, `conjecto_templates.py`) têm 500+ linhas cada um, misturando:
- ❌ UI com lógica de negócio
- ❌ Autenticação com manipulação de dados  
- ❌ Handlers espalhados sem organização

**Nossa solução:**
- ✅ **Core**: Apenas ciclo de vida da aplicação
- ✅ **Pages**: Apenas lógica de apresentação
- ✅ **Services**: Apenas lógica de negócio
- ✅ **Components**: Apenas elementos UI reutilizáveis

### 2. **Reduz Acoplamento Mantendo Legibilidade**
**Problema atual:** Funções gigantes como `make_side_panel()` fazem tudo
```python
# ❌ Seu código atual - acoplado
def make_side_panel(df, q, sp_title, dim_y, dim_x, group, plot_type, md_table_context):
    # 50+ linhas misturando dados, UI e lógica
```

**Nossa solução:** Responsabilidades separadas mas coesas
```python
# ✅ Nossa template - desacoplado mas legível
class SidePanelComponent(BaseComponent):
    def render(self, data): # Apenas renderização
        return self.create_panel(data)

class DataService:
    def process_dataframe(self, df): # Apenas processamento
        return processed_data

class DashboardPage(BasePage):
    async def render(self, q): # Apenas orquestração
        data = self.data_service.process_dataframe(df)
        panel = self.side_panel.render(data)
        self.add_card(q, 'panel', panel)
```

### 3. **Facilita Manutenção**
**Problema atual:** Para mudar um gráfico, você precisa mexer em:
- Função de 100+ linhas
- Lógica de dados misturada
- UI acoplada com backend

**Nossa solução:**
- 📁 **Mudar dados**: Apenas `services/data_service.py`
- 🎨 **Mudar UI**: Apenas `components/charts.py`  
- 🔀 **Mudar fluxo**: Apenas `pages/dashboard.py`
- 🔐 **Mudar auth**: Apenas `auth/manager.py`

### 4. **Reutilização Real**
No seu código atual, se quiser usar `make_bignumbers_st()` em outro app, precisa copiar:
- A função inteira
- Todas as dependências  
- Ajustar para novo contexto

**Nossa template:**
```python
# Usar em qualquer app
from components import StatsComponent
stats = StatsComponent()
card = stats.render(data)  # Funciona em qualquer lugar
```

### 5. **Equilibrio Perfeito**
**Muito desacoplado** = 50 arquivos pequenos, difícil de entender  
**Muito acoplado** = 1 arquivo gigante, difícil de manter

**Nossa abordagem:**
- 📝 **Páginas** = 1 arquivo por funcionalidade principal
- 🧩 **Componentes** = 1 arquivo por tipo de elemento
- ⚙️ **Core** = Apenas arquivos essenciais (3-4 arquivos)
- 🔧 **Utils** = Helpers organizados por propósito

**Resultado:** 15-20 arquivos bem organizados vs 3 arquivos gigantes

## 🚀 Como Usar

### 1. Instalação
```bash
pip install h2o-wave pandas
```

### 2. Configuração
Edite `core/config.py` com suas configurações:
```python
APP_NAME = "Minha Aplicação"
APP_VERSION = "1.0.0"
THEME = "neon"
```

### 3. Executar Aplicação
```bash
python app.py
```

### 4. Criar Nova Página
```python
from pages.base import BasePage
from h2o_wave import ui

class MinhaNovaPage(BasePage):
    def __init__(self, app):
        super().__init__(app, "minha_pagina", "Minha Página")
    
    async def render(self, q):
        return [
            ui.form_card(
                box="content",
                items=[
                    ui.text("Olá mundo!")
                ]
            )
        ]
```

### 5. Adicionar Componente
```python
from components.base import BaseComponent
from h2o_wave import ui

class MeuComponente(BaseComponent):
    def render(self, data=None):
        return ui.stat_card(
            box="stats",
            title="Estatística",
            value=str(data or 0)
        )
```

## 📝 Exemplo Simples

Veja o exemplo completo na aplicação incluída que demonstra:
- Sistema de login
- Dashboard com gráficos
- Componentes reutilizáveis
- Navegação entre páginas

## 🔧 Extensões

### Adicionar Nova Autenticação
1. Implemente `AuthProvider` em `auth/manager.py`
2. Configure em `core/config.py`
3. Use em qualquer página

### Adicionar Novo Serviço
1. Crie arquivo em `services/`
2. Herde de `BaseService` se necessário
3. Injete onde precisar

### Personalizar Tema
1. Modifique `core/config.py`
2. Adicione CSS customizado em `static/css/`
3. Configure layouts em `core/app.py`

## 🎨 Temas Suportados
- `neon` (padrão)
- `nord`
- `light`
- `dark`

## 📚 Documentação

- [H2O Wave Docs](https://wave.h2o.ai/)
- [Exemplos Avançados](./examples/)
- [API Reference](./docs/api.md)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

MIT License - veja LICENSE para detalhes.
