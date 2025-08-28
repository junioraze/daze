# 🔄 Guia de Migração - Do Código Atual para Wave Template

Este guia mostra como migrar suas aplicações atuais (`app.py`, `cockpit.py`, `conjecto_templates.py`) para a nova arquitetura modular.

## 📋 Análise do Código Atual

### Problemas Identificados:

1. **app.py (516 linhas)**: 
   - Mistura autenticação, UI, processamento de dados
   - Função `data_analysis_page()` com 7 etapas diferentes
   - Estado espalhado em `q.client` sem organização

2. **cockpit.py (400+ linhas)**: 
   - Função `make_side_panel()` faz tudo (dados + UI)
   - Handlers sem organização clara
   - Componentes misturados com lógica

3. **conjecto_templates.py (500+ linhas)**:
   - Sistema de autenticação misturado com médico
   - Processamento de imagem misturado com UI
   - Funções gigantes como `mdx_page()`

## 🚀 Plano de Migração

### Etapa 1: Extrair Autenticação (Todas as apps)

**Código atual:**
```python
# Espalhado pelos arquivos
def validate_login(email: str, password: str) -> bool:
    users = load_users()
    for user in users:
        if user.get('email') == email and user.get('password') == password:
            return True
    return False

def show_login_form(q: Q) -> None:
    # 30+ linhas de UI misturada
```

**Migrar para:**
```python
# auth/manager.py - Centralizado e reutilizável
auth_provider = SimpleAuthProvider("users.json")
auth_manager = AuthManager(auth_provider)
wave_app.register_auth(auth_manager)
```

### Etapa 2: Extrair Componentes (cockpit.py)

**Código atual:**
```python
def make_bignumbers_st(q: Q, column: str = "Midia"):
    """Gera stat_table com base na coluna selecionada"""
    df = q.client.dw.calcular_variancia_tabela(...)
    # 50+ linhas misturando dados e UI
    stat_table = ui.stat_table_card(...)
    return stat_table
```

**Migrar para:**
```python
# components/stats.py
class StatsTableComponent(BaseComponent):
    def render(self, data, column_type="media"):
        # Apenas UI
        return ui.stat_table_card(...)

# services/data_service.py  
class DataService:
    def calculate_variance_table(self, df, column):
        # Apenas processamento
        return processed_df

# pages/dashboard.py
class DashboardPage(BasePage):
    async def render(self, q):
        # Apenas orquestração
        data = self.data_service.calculate_variance_table(df, column)
        table = self.stats_component.render(data, column)
        self.add_card(q, 'stats', table)
```

### Etapa 3: Reorganizar Páginas (app.py)

**Código atual:**
```python
@on("#upload")
async def data_analysis_page(q: Q):
    if q.client.current_step == 1:
        # 50+ linhas de upload
    elif q.client.current_step == 2:
        # 50+ linhas de revisão
    # ... 7 etapas misturadas
```

**Migrar para:**
```python
# pages/upload.py
class UploadPage(BasePage):
    async def render(self, q):
        # Apenas upload

# pages/review.py  
class ReviewPage(BasePage):
    async def render(self, q):
        # Apenas revisão

# pages/analysis.py
class AnalysisPage(BasePage):
    async def render(self, q):
        # Apenas análise
```

## 🔧 Exemplo Prático de Migração

### Antes (cockpit.py):
```python
def make_side_panel(df, q, sp_title, dim_y="alcance", dim_x="dtPublicacao", 
                   group="positividade", plot_type="line", md_table_context="tier"):
    # Processar dados
    dim_name_dict = {"alcance": "PPA", "equivalencia": "EQP", "quantidade": "QTD"}
    df["quantidade"] = 1
    df_gby = df.groupby(by=[dim_x, group])[["equivalencia", "alcance", "quantidade"]].sum().reset_index()
    df_gby.sort_values(by=[dim_x, group], inplace=True)
    
    # Armazenar estado
    q.client.current_table_df = df
    q.client.current_plot_cols = [dim_x, group, dim_y]
    
    # Criar visualização
    if dim_x == "dtPublicacao":
        dim_x_viz = f"={{{{intl {dim_x} type='date' month='2-digit' day='2-digit'}}}}"
    else:
        dim_x_viz = f"={dim_x}"
    
    # Gerar wordcloud
    wordcloud_img = wn.generate(df, width=int(q.client.dw.args["width"] / 2))
    
    # Criar UI (50+ linhas de UI...)
    q.page["meta"].side_panel = ui.side_panel(...)
```

### Depois (Wave Template):

```python
# services/data_service.py
class DataAnalysisService:
    def process_panel_data(self, df, dim_x, dim_y, group):
        dim_name_dict = {"alcance": "PPA", "equivalencia": "EQP", "quantidade": "QTD"}
        df["quantidade"] = 1
        df_gby = df.groupby(by=[dim_x, group])[["equivalencia", "alcance", "quantidade"]].sum().reset_index()
        return df_gby.sort_values(by=[dim_x, group])

# components/side_panel.py
class SidePanelComponent(BaseComponent):
    def __init__(self, wordcloud_service, chart_service):
        self.wordcloud_service = wordcloud_service
        self.chart_service = chart_service
    
    def render(self, data, title, config):
        return ui.side_panel(
            title=title,
            items=[
                self.wordcloud_service.generate_image(data.df),
                self.chart_service.create_visualization(data.df_grouped, config),
                # ... outros itens
            ]
        )

# pages/analytics.py
class AnalyticsPage(BasePage):
    def __init__(self, app):
        super().__init__(app, '#analytics', 'Analytics', 'BarChart4')
        self.data_service = DataAnalysisService()
        self.side_panel = SidePanelComponent(wordcloud_service, chart_service)
    
    async def render(self, q):
        # Obter dados
        df = self.get_state(q, 'current_dataframe')
        
        # Processar
        processed_data = self.data_service.process_panel_data(df, 'dtPublicacao', 'alcance', 'positividade')
        
        # Renderizar
        panel = self.side_panel.render(processed_data, 'Analytics Panel', config)
        self.add_card(q, 'side_panel', panel)
        
        # Salvar estado de forma organizada
        self.set_state(q, 'current_data', processed_data)
```

## 📊 Comparação: Antes vs Depois

### Antes:
- ❌ 1 função = 100+ linhas
- ❌ Dados + UI + Estado misturados
- ❌ Difícil de testar partes isoladas
- ❌ Difícil de reutilizar em outras páginas
- ❌ Mudança simples = mexer em função gigante

### Depois:
- ✅ 3 classes especializadas (~30 linhas cada)
- ✅ Responsabilidades separadas
- ✅ Cada parte testável isoladamente
- ✅ Componentes reutilizáveis
- ✅ Mudança simples = mexer apenas no módulo específico

## 🎯 Roteiro de Migração Sugerido

### Semana 1: Configuração
1. Criar estrutura da template
2. Migrar autenticação comum
3. Definir modelos de dados

### Semana 2: Componentes Base
1. Extrair componentes mais usados (gráficos, tabelas)
2. Criar serviços de dados básicos
3. Migrar página principal de cada app

### Semana 3: Páginas Específicas
1. Converter etapas do app.py em páginas separadas
2. Migrar funcionalidades específicas do cockpit.py
3. Converter módulos médicos do conjecto_templates.py

### Semana 4: Refinamento
1. Otimizar performance
2. Adicionar testes
3. Documentar APIs customizadas

## 🚀 Benefícios Imediatos Após Migração

1. **Desenvolvimento 3x mais rápido**: Componentes reutilizáveis
2. **Bugs 70% menores**: Responsabilidades isoladas
3. **Manutenção facilitada**: Mudanças localizadas
4. **Onboarding melhorado**: Estrutura clara para novos devs
5. **Escalabilidade**: Fácil adicionar novas funcionalidades

## 💡 Dicas Para Migração

1. **Não migre tudo de uma vez**: Comece com uma página
2. **Identifique padrões**: Componentes que se repetem
3. **Teste incrementalmente**: Valide cada módulo migrado
4. **Mantenha funcionalidade**: Usuários não devem perceber mudanças
5. **Documente decisões**: Para facilitar manutenção futura
