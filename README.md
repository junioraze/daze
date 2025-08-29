# DAZE - H2O Wave Template
*Dynamic Application Zone Engine - Template modular para projetos H2O Wave*

## 🎯 O que é o DAZE?

DAZE é um template produção-ready para H2O Wave que oferece:

- **Arquitetura Modular**: Cards flexíveis que orquestram múltiplos componentes
- **Componentes Reutilizáveis**: Gráficos, estatísticas, tabelas com métodos `create()` e `update()`
- **Sistema de Eventos**: Gerenciamento inteligente de interações do usuário
- **Compatibilidade Total**: 100% compatível com H2O Wave UI
- **Pronto para Produção**: Estrutura escalável e organizada

## 🏗️ Arquitetura

```
DAZE/
├── components/
│   ├── base.py          # BaseComponent e BaseCard
│   ├── charts.py        # Componente de gráficos
│   ├── stats.py         # Componente de estatísticas
│   └── tables.py        # Componente de tabelas
├── pages/
│   └── base.py          # BasePage para layout
├── services/
│   └── data_service.py  # Serviços de dados
└── main.py              # Exemplo funcional
```
### Conceitos Principais

1. **BaseComponent**: Classe abstrata para componentes reutilizáveis
2. **BaseCard**: Container que orquestra múltiplos componentes
3. **BasePage**: Gerencia layout e cards
4. **DataService**: Processa dados e converte para Wave

## 🚀 Início Rápido

### Instalação
```bash
pip install h2o-wave
```

### Executar Exemplo
```bash
wave run main.py
```

### Criar Sua Primeira Aplicação

```python
from h2o_wave import app, Q
from core.app import WaveApp
from pages.base import BasePage
from components.base import BaseComponent, BaseCard

class MyComponent(BaseComponent):
    def render(self, q, state=None):
        q.page[self.component_id] = ui.form_card(
            box='1 1 2 2',
            items=[
                ui.text_l('Exemplo DAZE!'),
                ui.textbox(name='dummy', label='Digite algo', visible=True),
                ui.button(name='meu_evento', label='Enviar', primary=True)
            ]
        )
        # Exibe resultado do evento
        result = self.get_result(q, 'meu_evento')
        if result:
            q.page['result'] = ui.markdown_card(box='1 3 2 1', title='Resultado', content=result)

    def on_meu_evento(self, q, state=None, args=None):
        valor = args.get('dummy')
        return f'Você digitou: {valor}'

class MyCard(BaseCard):
    def __init__(self, card_id):
        super().__init__(card_id)
        self.add_component('main', MyComponent('main'))

class MyPage(BasePage):
    def __init__(self, page_id):
        super().__init__(page_id, title='Minha Página')
        self.add_card('main', MyCard('main'))

app_daze = WaveApp()
app_daze.add_page('main', MyPage('main'))
app_daze.register_wave_event('meu_evento')

@app("/")
async def serve(q: Q):
    args = app_daze.get_args(q)
    if args:
        q.client.last_event = args.copy() if hasattr(args, 'copy') else dict(args)
    await app_daze.handle_events(q, args=args)
    app_daze.render(q)
    await q.page.save()
                'box': 'content',
                'title': 'Vendas'
            }
        }
        super().create(q, zone, **dados_iniciais)
    
    async def _handle_update(self, q: Q):
        # Atualizar dados
        novos_dados = {
            'grafico': {
                'chart_data': [{'x': 'A', 'y': 200}],
                'box': 'content',
                'title': 'Vendas Atualizadas'
            }
        }
        self.update_components(q, novos_dados)

# 2. Criar Página
class MinhaPagina(BasePage):
    def __init__(self):
        super().__init__(route='/', title='Minha App')
        self.meu_card = MeuCard()
        self.add_card(self.meu_card, 'content')
    
    async def handle_events(self, q):
        return await self.meu_card.handle_events(q)

# 3. Servir
pagina = MinhaPagina()

@app('/')
async def serve(q: Q):
    if await pagina.handle_events(q):
        await q.page.save()
        return
    await pagina.render(q)

if __name__ == '__main__':
    main()
```

## 📋 Componentes Disponíveis

### ChartComponent
```python
chart = ChartComponent('meu_grafico')
chart_data = [{'x': 'Jan', 'y': 100}, {'x': 'Feb', 'y': 150}]
chart.create(q, chart_data=chart_data, box='content', title='Vendas')
chart.update(q, chart_data=novos_dados)
```

### StatsComponent
```python
stats = StatsComponent('minhas_stats')
stats_data = [
    {'label': 'Vendas', 'value': '1000', 'icon': 'Money'},
    {'label': 'Clientes', 'value': '50', 'icon': 'People'}
]
stats.create(q, stats_data=stats_data, box='sidebar')
```

### TableComponent
```python
table = TableComponent('minha_tabela')
table_data = [
    {'produto': 'A', 'vendas': 100},
    {'produto': 'B', 'vendas': 200}
]
table.create(q, table_data=table_data, box='content', title='Produtos')
```

## 🎛️ Sistema de Eventos

### Registrar Eventos no Card
```python
class MeuCard(BaseCard):
    def __init__(self):
        super().__init__('card_id')
        
        # Registrar handlers
        self.register_event('botao_click', self._handle_click)
        self.register_event('refresh', self._handle_refresh)
    
    async def _handle_click(self, q: Q):
        # Lógica do evento
        pass
```

### Sistema Automático de Detecção
O BaseCard automaticamente detecta eventos baseado nos nomes dos botões/controles.

## 🔧 Personalização Avançada

### Criar Componente Personalizado
```python
from components.base import BaseComponent

class MeuComponente(BaseComponent):
    def create(self, q: Q, **kwargs):
        dados = kwargs.get('meus_dados', [])
        box = kwargs.get('box', 'content')
        title = kwargs.get('title', 'Meu Componente')
        
        # Criar UI específica
        q.page[self.component_id] = ui.form_card(
            box=box,
            title=title,
            items=[ui.text(f'Dados: {len(dados)} itens')]
        )
    
    def update(self, q: Q, **kwargs):
        # Re-criar com novos dados
        self.create(q, **kwargs)
```

### Layout Personalizado
```python
class MinhaPagina(BasePage):
    def setup_layout(self, q: Q):
        q.page['sidebar'] = ui.nav_card(box='1 1 2 -1', items=[])
        q.page['header'] = ui.header_card(box='3 1 -1 2', title='App')
        q.page['content'] = ui.form_card(box='3 3 -1 -1', title='Conteúdo')
```

## 📊 Trabalhando com Dados

### DataService
```python
from services.data_service import DataService

data_service = DataService()

# Converter dados para Wave charts
chart_data = data_service.to_wave_data(meus_dados, x='mes', y='vendas')

# Processar dados
```

### Integração com APIs
```python
class MeuCard(BaseCard):
    async def _fetch_data(self):
        dados = await self._fetch_data()
        self.update_components(q, {'chart': {'chart_data': dados}})
```

## 🎨 Boas Práticas

### Organização de Cards
- Um card = um conjunto lógico de funcionalidades
- Cards orquestram múltiplos componentes relacionados
- Use eventos para coordenar atualizações

### Gerenciamento de Estado
- Use `q.client` para estado por sessão
- Cards mantêm referências aos componentes
- DataService processa e converte dados

### Performance
- Atualize apenas componentes necessários
- Use `update_components()` com dados específicos
- Evite re-criar toda a página desnecessariamente

## 🚀 Deploy para Produção

### Estrutura Recomendada
```
minha_app/
├── components/       # Componentes reutilizáveis
├── pages/           # Páginas da aplicação
├── services/        # Lógica de negócio
├── static/          # Arquivos estáticos
├── config/          # Configurações
└── main.py          # Ponto de entrada
```

### Configuração
```python
# config/settings.py
WAVE_CONFIG = {
    'host': '0.0.0.0',
    'port': 10101,
    'debug': False
}
```

## 🤝 Contribuindo

DAZE é um template base - customize e expanda conforme suas necessidades!

---
# DAZE - H2O Wave Template (Atualizado)
---

**DAZE** - Accelerating Wave Development 🌊⚡
3. Implemente `handle_events()` para responder a eventos do usuário.

## Como rodar
## Recomendações
- Use sempre o serviço de dados para acessar e manipular dados.
- Mantenha o estado do usuário em `q.client`.
- Use os utilitários do BaseCard para criar componentes Wave de forma simples.
- Siga o padrão de eventos para atualização dinâmica dos cards.

---

Para dúvidas ou sugestões, consulte o arquivo MIGRATION.md ou abra uma issue.
