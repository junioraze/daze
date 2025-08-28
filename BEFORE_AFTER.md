# 🔄 Exemplos Antes e Depois - Transformação de Código

## 🎯 Objetivo

Este documento mostra **transformações práticas** do seu código atual aplicando os conceitos da Wave Template. Cada exemplo é extraído dos seus arquivos reais.

---

## 1. 📊 Transformação: Gerenciamento de Estado

### ❌ **ANTES** (do seu `app.py`)
```python
def initialize_client(q: Q) -> None:
    """Inicializa o cliente com valores padrão"""
    q.client.cards = set()
    q.client.uploaded_files = []
    q.client.selected_file = ""
    q.client.dataframe = None
    q.client.scored_dataframe = None
    q.client.current_step = 1
    q.client.score_column = "risk_score"
    q.client.chart_city_state = None
    q.client.selected_column = None
    q.client.dre_risk_range = "medio"
    q.client.logo_url = "logo_mc.jpeg"
    q.client.wide_logo_url = "wide_logo_mc.png"
    q.client.valor_minimo_divida = 1000.0
    q.client.maximo_meses_atraso = 60
    q.client.editing_valor_minimo = False
    q.client.editing_filtros = False
    q.client.data_filtered = False
    q.client.dataframe_original = None

def get_safe_value(client, attr_name: str, default_value):
    """Obtém valor do cliente de forma segura"""
    return getattr(client, attr_name, default_value)
```

**Problemas:**
- 20+ variáveis espalhadas em `q.client`
- Sem tipagem ou validação
- Difícil de rastrear mudanças
- Sem organização lógica

### ✅ **DEPOIS** (Wave Template)
```python
# core/state.py
class StateManager:
    """Gerenciador de estado centralizado e tipado"""
    
    def initialize_client(self, q: Q) -> None:
        if not hasattr(q.client, 'initialized'):
            q.client.initialized = True
            q.client.app_state = AppState()
            q.client.tracked_cards = set()

    def set_client_state(self, q: Q, key: str, value: Any) -> None:
        state = self.get_client_state(q)
        state[key] = value
    
    def get_client_value(self, q: Q, key: str, default: Any = None) -> Any:
        state = self.get_client_state(q)
        return state.get(key, default)

# models/app_state.py
@dataclass
class AppState:
    """Estado tipado da aplicação"""
    current_step: int = 1
    uploaded_files: List[str] = field(default_factory=list)
    selected_file: str = ""
    dataframe: Optional[pd.DataFrame] = None
    filters: FilterConfig = field(default_factory=FilterConfig)
    ui_config: UIConfig = field(default_factory=UIConfig)

@dataclass
class FilterConfig:
    valor_minimo_divida: float = 1000.0
    maximo_meses_atraso: int = 60
    data_filtered: bool = False

@dataclass  
class UIConfig:
    logo_url: str = "logo_mc.jpeg"
    wide_logo_url: str = "wide_logo_mc.png"
    theme: str = "neon"
```

**Melhorias:**
- ✅ Estado tipado e validado
- ✅ Organização lógica em classes
- ✅ Métodos centralizados para acesso
- ✅ Fácil de testar e debugar

---

## 2. 🎨 Transformação: Componentes UI

### ❌ **ANTES** (do seu `cockpit.py`)
```python
def make_side_panel(
    df: pd.DataFrame,
    q: Q,
    sp_title: str,
    dim_y: str = "alcance",
    dim_x: str = "dtPublicacao",
    group: str = "positividade",
    plot_type: str = "line",
    md_table_context: str = "tier",
):
    # 20 linhas processando dados
    dim_name_dict = {"alcance": "PPA", "equivalencia": "EQP", "quantidade": "QTD"}
    df["quantidade"] = 1
    df_gby = (
        df.groupby(by=[dim_x, group])[["equivalencia", "alcance", "quantidade"]]
        .sum()
        .reset_index()
    )
    df_gby.sort_values(by=[dim_x, group], inplace=True)
    q.client.current_table_df = df
    q.client.current_plot_cols = [dim_x, group, dim_y]
    q.client.current_md_table_context = md_table_context
    
    # 15 linhas configurando visualização
    if dim_x == "dtPublicacao":
        dim_x_viz = f"={{{{intl {dim_x} type='date' month='2-digit' day='2-digit'}}}}"
    else:
        dim_x_viz = f"={dim_x}"
    plot_colors = pc.get_plot_color(group)
    q.page["meta"].script = ui.inline_script(_js_screen)
    
    # 50+ linhas criando UI
    q.page["meta"].side_panel = ui.side_panel(
        name="side_panel",
        events=["dismissed"],
        title=sp_title,
        closable=True,
        width="100%",
        items=[
            ui.image(
                title="wordcloud",
                image=wn.generate(
                    df,
                    width=int(q.client.dw.args["width"] / 2),
                ),
                width=str(q.client.dw.args["width"]) + "px"
                if q.client.dw.args["width"] < 1100
                else "1500px",
                type="png",
            ),
            # ... mais 40 linhas de UI
        ],
    )
```

**Problemas:**
- 100+ linhas em uma função
- Dados + UI + Estado misturados
- Difícil de testar partes isoladas
- Impossível de reutilizar

### ✅ **DEPOIS** (Wave Template)
```python
# services/analytics_service.py
class AnalyticsService:
    """Serviço responsável APENAS por processamento de dados"""
    
    def process_panel_data(
        self, 
        df: pd.DataFrame, 
        config: PanelConfig
    ) -> PanelData:
        dim_name_dict = {"alcance": "PPA", "equivalencia": "EQP", "quantidade": "QTD"}
        df["quantidade"] = 1
        
        df_grouped = (
            df.groupby(by=[config.dim_x, config.group])
            [["equivalencia", "alcance", "quantidade"]]
            .sum()
            .reset_index()
        )
        
        return PanelData(
            original_df=df,
            grouped_df=df_grouped.sort_values(by=[config.dim_x, config.group]),
            dimensions=dim_name_dict
        )

# components/side_panel.py
class SidePanelComponent(BaseComponent):
    """Componente responsável APENAS por renderização"""
    
    def __init__(self, wordcloud_service: WordCloudService, chart_service: ChartService):
        self.wordcloud_service = wordcloud_service
        self.chart_service = chart_service
    
    def render(self, data: PanelData, config: PanelConfig) -> ui.FormCard:
        return ui.side_panel(
            name="side_panel",
            title=config.title,
            closable=True,
            width="100%",
            items=[
                self._create_wordcloud(data.original_df, config),
                self._create_chart(data.grouped_df, config),
                self._create_summary_table(data, config)
            ]
        )
    
    def _create_wordcloud(self, df: pd.DataFrame, config: PanelConfig) -> ui.Component:
        return ui.image(
            title="wordcloud",
            image=self.wordcloud_service.generate(df, width=config.width),
            type="png"
        )

# pages/analytics_page.py
class AnalyticsPage(BasePage):
    """Página responsável APENAS por orquestração"""
    
    def __init__(self, app: WaveApp):
        super().__init__(app, '#analytics', 'Analytics', 'BarChart4')
        self.analytics_service = AnalyticsService()
        self.side_panel = SidePanelComponent(wordcloud_service, chart_service)
    
    async def render(self, q: Q) -> None:
        # Obter configuração
        config = self.get_panel_config(q)
        
        # Processar dados
        data = self.analytics_service.process_panel_data(
            df=self.get_dataframe(q),
            config=config
        )
        
        # Renderizar UI
        panel = self.side_panel.render(data, config)
        self.add_card(q, 'side_panel', panel)
        
        # Salvar estado
        self.set_state(q, 'panel_data', data)

# models/panel_models.py
@dataclass
class PanelConfig:
    title: str
    dim_x: str = "dtPublicacao"
    dim_y: str = "alcance"
    group: str = "positividade"
    plot_type: str = "line"
    width: int = 800

@dataclass
class PanelData:
    original_df: pd.DataFrame
    grouped_df: pd.DataFrame
    dimensions: Dict[str, str]
```

**Melhorias:**
- ✅ Separação clara: Dados / UI / Orquestração
- ✅ Cada classe tem responsabilidade única
- ✅ Testável isoladamente
- ✅ Reutilizável em outras páginas
- ✅ Tipado e documentado

---

## 3. 🔐 Transformação: Sistema de Autenticação

### ❌ **ANTES** (do seu `conjecto_templates.py`)
```python
def load_users():
    """Carrega usuários do arquivo JSON"""
    try:
        with open('auth_users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('users', [])
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        return []

def validate_login(email: str, password: str) -> bool:
    """Valida as credenciais de login"""
    users = load_users()
    for user in users:
        if user.get('email') == email and user.get('password') == password:
            return True
    return False

def create_login_form_items(email: str = "", show_error: bool = False) -> list:
    """Cria os itens do formulário de login reutilizável"""
    items = [
        ui.text_xl("🏥 MDX XRay - Login"),
        ui.separator(),
    ]
    
    if show_error:
        items.append(ui.message_bar(type='error', text='Email ou senha incorretos!'))
    
    items.extend([
        ui.textbox(name="email", label="Email", ...),
        ui.textbox(name="password", label="Senha", password=True, ...),
        ui.buttons([ui.button(name="login_submit", ...)]),
    ])
    return items

def show_login_form(q: Q) -> None:
    """Exibe o formulário de login"""
    q.page["meta"] = ui.meta_card(...)
    q.page["login_form"] = ui.form_card(
        box="main",
        items=create_login_form_items()
    )

# Handler global misturado com outras coisas
if q.args.login_submit:
    email = q.args.email
    password = q.args.password
    if validate_login(email, password):
        # Lógica de sucesso misturada
        pass
    else:
        # Lógica de erro misturada
        pass
```

**Problemas:**
- Lógica de auth espalhada por todo código
- UI misturada com lógica de negócio
- Sem abstração para diferentes tipos de auth
- Difícil de testar e modificar

### ✅ **DEPOIS** (Wave Template)
```python
# auth/models.py
@dataclass
class User:
    """Modelo tipado de usuário"""
    id: str
    username: str
    email: str
    full_name: str = ""
    is_active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(**data)

# auth/providers.py
class AuthProvider(ABC):
    """Interface para diferentes tipos de autenticação"""
    
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[User]:
        pass

class SimpleAuthProvider(AuthProvider):
    """Implementação para autenticação simples"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self._users: Dict[str, User] = {}
        self._load_users()
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        for user in self._users.values():
            if (user.username == username or user.email == username) and user.is_active:
                # Aqui validaria senha hash
                user.last_login = datetime.now()
                self._save_users()
                return user
        return None

class OAuthProvider(AuthProvider):
    """Implementação para OAuth (Google, Microsoft, etc.)"""
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        # Implementação OAuth
        pass

# auth/manager.py
class AuthManager:
    """Gerenciador central de autenticação"""
    
    def __init__(self, provider: AuthProvider):
        self.provider = provider
    
    async def is_authenticated(self, q: Q) -> bool:
        return hasattr(q.client, 'user') and q.client.user is not None
    
    async def get_current_user(self, q: Q) -> Optional[User]:
        return getattr(q.client, 'user', None)
    
    async def login(self, q: Q, username: str, password: str) -> bool:
        user = await self.provider.authenticate(username, password)
        if user:
            q.client.user = user
            q.client.authenticated = True
            return True
        return False
    
    async def logout(self, q: Q) -> None:
        if hasattr(q.client, 'user'):
            delattr(q.client, 'user')
        q.client.authenticated = False

# components/login_form.py
class LoginFormComponent(BaseComponent):
    """Componente responsável APENAS pela UI de login"""
    
    def render(self, show_error: bool = False, email: str = "") -> ui.FormCard:
        items = [
            ui.text_xl("🔐 Login"),
            ui.separator()
        ]
        
        if show_error:
            items.append(ui.message_bar(type='error', text='Credenciais inválidas!'))
        
        items.extend([
            ui.textbox('username', 'Usuário', value=email, required=True),
            ui.textbox('password', 'Senha', password=True, required=True),
            ui.buttons([
                ui.button('login_submit', 'Entrar', primary=True, icon='SignIn')
            ], justify='center')
        ])
        
        return ui.form_card(box='content', items=items)

# core/app.py - Integração limpa
class WaveApp:
    def register_auth(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager
    
    async def init_client(self, q: Q) -> None:
        self.state_manager.initialize_client(q)
        
        if self.config.auth_enabled and self.auth_manager:
            if not await self.auth_manager.is_authenticated(q):
                await self.show_login_page(q)
                return
        
        await self.navigate_to_page(q, self.get_default_route())

# app.py - Handler clean
@app('/')
async def serve(q: Q):
    if q.args.login_submit:
        success = await wave_app.auth_manager.login(q, q.args.username, q.args.password)
        if success:
            await wave_app.navigate_to_page(q, '#dashboard')
        else:
            q.client.login_error = True
            await wave_app.show_login_page(q)
        await q.page.save()
        return
    
    await run_on(q)
    await q.page.save()
```

**Melhorias:**
- ✅ Separação clara: Models / Providers / Manager / Components
- ✅ Suporte a múltiplos tipos de auth (Simple, OAuth, LDAP)
- ✅ UI completamente isolada da lógica
- ✅ Fácil de testar cada parte
- ✅ Fácil de trocar implementação

---

## 4. 📋 Transformação: Manipulação de Páginas

### ❌ **ANTES** (do seu `app.py`)
```python
@on("#upload")
async def data_analysis_page(q: Q):
    """Página principal com sistema de 4 etapas para análise de dados"""
    clear_cards(q)

    if not hasattr(q.client, 'current_step'):
        q.client.current_step = 1

    # Step 1: Upload de Arquivos CSV/Excel
    if q.client.current_step == 1:
        navigation = create_step_navigation(q)
        
        q.page['step_content'] = ui.form_card(
            box="main_content",
            items=navigation + [
                ui.text_xl('📤 Passo 1: Upload de Arquivos'),
                ui.text('Envie seus arquivos CSV ou Excel para análise.'),
                ui.separator(),
                ui.file_upload(
                    name='file_upload',
                    label='Selecionar Arquivos',
                    multiple=True,
                    file_extensions=['csv', 'xlsx', 'xls'],
                    max_file_size=100,
                    height='200px'
                ),
                ui.separator(),
                ui.text_s('💡 **Formatos aceitos:** CSV, Excel (.xlsx, .xls)'),
                ui.text_s('📏 **Tamanho máximo:** 100MB por arquivo'),
                # ... mais 50 linhas para Step 1
            ]
        )
        
    elif q.client.current_step == 2:
        # ... mais 100 linhas para Step 2
        navigation = create_step_navigation(q)
        
        if q.client.dataframe is not None and not q.client.dataframe.empty:
            df = q.client.dataframe
            # Lógica de revisão de dados (50+ linhas)
            q.page['step_content'] = ui.form_card(...)
        
    elif q.client.current_step == 3:
        # ... mais 100 linhas para Step 3
        pass
        
    elif q.client.current_step == 4:
        # ... mais 100 linhas para Step 4
        pass
        
    elif q.client.current_step == 5:
        # ... mais 100 linhas para Step 5
        pass
        
    # Total: 500+ linhas em uma função
```

**Problemas:**
- 500+ linhas em uma função
- 7 etapas diferentes misturadas
- Difícil de manter e debugar
- Impossível de testar etapas isoladas

### ✅ **DEPOIS** (Wave Template)
```python
# pages/base.py
class BasePage(ABC):
    """Classe base para todas as páginas"""
    
    def __init__(self, app: WaveApp, route: str, title: str, icon: str = 'Page'):
        self.app = app
        self.route = route
        self.title = title
        self.icon = icon
    
    @abstractmethod
    async def render(self, q: Q) -> None:
        pass
    
    # Métodos auxiliares compartilhados
    def add_card(self, q: Q, name: str, card: ui.FormCard) -> None:
        q.page[name] = card
        self.app.state_manager.add_card(q, name)

# pages/upload_page.py
class UploadPage(BasePage):
    """Página responsável APENAS por upload de arquivos"""
    
    def __init__(self, app: WaveApp):
        super().__init__(app, '#upload', 'Upload', 'Upload')
        self.file_service = FileService()
    
    async def render(self, q: Q) -> None:
        self.add_card(q, 'upload_form', ui.form_card(
            box="content",
            items=[
                ui.text_xl('📤 Upload de Arquivos'),
                ui.text('Envie seus arquivos CSV ou Excel para análise.'),
                ui.separator(),
                ui.file_upload(
                    name='file_upload',
                    label='Selecionar Arquivos',
                    multiple=True,
                    file_extensions=['csv', 'xlsx', 'xls'],
                    max_file_size=100,
                    height='200px'
                ),
                ui.separator(),
                ui.text_s('💡 **Formatos aceitos:** CSV, Excel (.xlsx, .xls)'),
                ui.buttons([
                    ui.button('process_files', 'Processar Arquivos', primary=True)
                ])
            ]
        ))

# pages/review_page.py
class ReviewPage(BasePage):
    """Página responsável APENAS por revisão dos dados"""
    
    def __init__(self, app: WaveApp):
        super().__init__(app, '#review', 'Revisão', 'View')
        self.data_service = DataService()
    
    async def render(self, q: Q) -> None:
        df = self.get_dataframe(q)
        
        if df is None or df.empty:
            self.show_error(q, "Nenhum dado encontrado. Faça upload primeiro.")
            return
        
        preview_data = self.data_service.create_preview(df)
        stats = self.data_service.calculate_basic_stats(df)
        
        self.add_card(q, 'data_preview', ui.form_card(
            box="content",
            items=[
                ui.text_xl('📋 Revisão dos Dados'),
                ui.text(f'📊 **{len(df):,} registros** em **{len(df.columns)} colunas**'),
                ui.separator(),
                ui.table(
                    name='preview_table',
                    columns=self._create_table_columns(df),
                    rows=preview_data,
                    height='400px'
                ),
                ui.separator(),
                self._create_stats_panel(stats),
                ui.buttons([
                    ui.button('goto_filters', 'Configurar Filtros', primary=True),
                    ui.button('goto_upload', 'Voltar ao Upload')
                ])
            ]
        ))

# pages/analysis_page.py  
class AnalysisPage(BasePage):
    """Página responsável APENAS por análise dos dados"""
    
    def __init__(self, app: WaveApp):
        super().__init__(app, '#analysis', 'Análise', 'BarChart4')
        self.analysis_service = AnalysisService()
        self.chart_component = ChartComponent()
    
    async def render(self, q: Q) -> None:
        df = self.get_filtered_dataframe(q)
        
        # Executar análise
        analysis_results = await self.analysis_service.run_analysis(df)
        
        # Renderizar resultados
        self.add_card(q, 'analysis_results', ui.form_card(
            box="content",
            items=[
                ui.text_xl('🎯 Resultados da Análise'),
                self.chart_component.render_score_distribution(analysis_results),
                self.chart_component.render_risk_matrix(analysis_results),
                ui.buttons([
                    ui.button('export_results', 'Exportar Resultados', icon='Download'),
                    ui.button('goto_visualization', 'Ver Visualizações', primary=True)
                ])
            ]
        ))

# core/app.py - Registro das páginas
class WaveApp:
    def __init__(self):
        # ... outros setups
        
        # Registrar páginas automaticamente
        self._setup_pages()
    
    def _setup_pages(self):
        """Configura todas as páginas da aplicação"""
        pages = [
            UploadPage(self),
            ReviewPage(self),
            FiltersPage(self),
            AnalysisPage(self),
            VisualizationPage(self),
            ReportsPage(self)
        ]
        
        for page in pages:
            self.register_page(page)

# app.py - Navegação clean
@app('/')
async def serve(q: Q):
    # Navegação simples baseada em rotas
    if q.route:
        await wave_app.navigate_to_page(q, q.route)
    
    # Handlers específicos
    if q.args.process_files:
        await handle_file_processing(q)
    elif q.args.apply_filters:
        await handle_filter_application(q)
    
    await run_on(q)
    await q.page.save()
```

**Melhorias:**
- ✅ Cada etapa = uma página separada (50-100 linhas cada)
- ✅ Responsabilidade única por página
- ✅ Navegação baseada em rotas clean
- ✅ Testável isoladamente
- ✅ Fácil adicionar/remover etapas

---

## 5. 🔧 Transformação: Tratamento de Erros

### ❌ **ANTES** (espalhado pelos seus arquivos)
```python
# Sem tratamento consistente
def load_data_file(file_path):
    df = pd.read_csv(file_path)  # Pode quebrar
    return df

# Tratamento básico  
def process_file_upload(q: Q):
    try:
        df = pd.read_excel(file_path)
        q.client.dataframe = df
    except Exception as e:
        print(f"Erro: {e}")  # Apenas print

# Erro silencioso
def apply_scoring_model(df):
    try:
        result = complex_calculation(df)
        return result
    except:
        return None  # Usuário não sabe que deu erro
```

### ✅ **DEPOIS** (Wave Template)
```python
# utils/exceptions.py
class AppException(Exception):
    """Exceção base da aplicação"""
    pass

class DataProcessingError(AppException):
    """Erro no processamento de dados"""
    pass

class FileFormatError(AppException):
    """Erro no formato do arquivo"""
    pass

class ValidationError(AppException):
    """Erro de validação"""
    pass

# services/data_service.py
class DataService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def load_data_file(self, file_path: str) -> pd.DataFrame:
        """Carrega arquivo com tratamento robusto de erros"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise FileFormatError(f"Formato não suportado: {file_ext}")
            
            # Validação básica
            if df.empty:
                raise ValidationError("Arquivo está vazio")
            
            if len(df.columns) < 2:
                raise ValidationError("Arquivo deve ter pelo menos 2 colunas")
            
            self.logger.info(f"Arquivo carregado: {len(df)} registros, {len(df.columns)} colunas")
            return df
            
        except pd.errors.EmptyDataError:
            raise FileFormatError("Arquivo CSV está vazio ou corrompido")
        except pd.errors.ParserError as e:
            raise FileFormatError(f"Erro ao analisar CSV: {str(e)}")
        except Exception as e:
            self.logger.error(f"Erro inesperado ao carregar {file_path}: {e}")
            raise DataProcessingError(f"Erro ao carregar arquivo: {str(e)}")

# pages/base.py - Tratamento na UI
class BasePage(ABC):
    def show_error(self, q: Q, error: str, error_type: str = "error") -> None:
        """Exibe erro de forma amigável ao usuário"""
        icon = "❌" if error_type == "error" else "⚠️"
        
        self.add_card(q, 'error_message', ui.form_card(
            box='content',
            items=[
                ui.message_bar(
                    type=error_type,
                    text=f'{icon} {error}',
                    buttons=[
                        ui.button('dismiss_error', 'OK', primary=True)
                    ]
                )
            ]
        ))
    
    def show_success(self, q: Q, message: str) -> None:
        """Exibe mensagem de sucesso"""
        self.add_card(q, 'success_message', ui.form_card(
            box='content',
            items=[
                ui.message_bar(
                    type='success', 
                    text=f'✅ {message}'
                )
            ]
        ))

# pages/upload_page.py - Uso do tratamento
class UploadPage(BasePage):
    async def handle_file_upload(self, q: Q) -> None:
        try:
            file_paths = convert_wave_file_paths(q.args.file_upload)
            
            for file_path in file_paths:
                df = await self.data_service.load_data_file(file_path)
                
                # Validação de negócio específica
                await self.validate_business_rules(df)
                
                # Sucesso
                self.set_state(q, 'dataframe', df)
                self.show_success(q, f"Arquivo carregado: {len(df):,} registros")
                
                # Navegar para próxima etapa
                await self.app.navigate_to_page(q, '#review')
                
        except FileFormatError as e:
            self.show_error(q, f"Formato de arquivo inválido: {e}", "warning")
        except ValidationError as e:
            self.show_error(q, f"Dados inválidos: {e}", "warning")
        except DataProcessingError as e:
            self.show_error(q, f"Erro no processamento: {e}")
            self.logger.error(f"Erro de processamento: {e}")
        except Exception as e:
            self.show_error(q, "Erro inesperado. Tente novamente.")
            self.logger.exception(f"Erro não tratado: {e}")

# core/app.py - Tratamento global
class WaveApp:
    async def navigate_to_page(self, q: Q, route: str) -> None:
        try:
            page = self.get_page(route)
            if not page:
                raise AppException(f"Página não encontrada: {route}")
            
            await page.render(q)
            await q.page.save()
            
        except AppException as e:
            self.logger.warning(f"Erro da aplicação: {e}")
            await self.show_error_page(q, str(e))
        except Exception as e:
            self.logger.exception(f"Erro crítico: {e}")
            await self.show_error_page(q, "Erro interno do sistema")
```

**Melhorias:**
- ✅ Hierarquia de exceções customizadas
- ✅ Logging estruturado em todos os níveis
- ✅ Mensagens amigáveis para usuário
- ✅ Tratamento específico por tipo de erro
- ✅ Recovery automático quando possível

---

## 🎯 Resumo das Transformações

| Aspecto | ❌ Antes | ✅ Depois |
|---------|----------|-----------|
| **Tamanho** | 3 arquivos de 500+ linhas | 15+ arquivos de 50-100 linhas |
| **Responsabilidades** | Tudo misturado | Separadas por domínio |
| **Estado** | 20+ variáveis em `q.client` | Classes tipadas organizadas |
| **Reutilização** | Copiar/colar funções | Componentes modulares |
| **Testes** | Impossível testar partes | Cada módulo testável |
| **Manutenção** | Mexer em funções gigantes | Editar módulo específico |
| **Onboarding** | Difícil entender fluxo | Estrutura clara e documentada |
| **Escalabilidade** | Limitada pela monoliticidade | Fácil adicionar funcionalidades |

## 🚀 Próximos Passos para Aplicar

1. **Escolha 1 função** do seu código atual (ex: `make_side_panel`)
2. **Identifique responsabilidades** (dados, UI, estado)  
3. **Separe em módulos** seguindo os exemplos acima
4. **Adicione tratamento de erros** robusto
5. **Teste** cada parte isoladamente
6. **Refatore** até ficar satisfeito
7. **Repita** para próxima função

**Lembre-se:** O objetivo é **dominar a metodologia**, não apenas aplicar mecanicamente! 💪
