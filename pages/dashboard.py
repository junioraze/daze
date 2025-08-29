from components.base import BaseCard

# Card de header modular
class DashboardHeaderCard(BaseCard):
    def __init__(self):
        super().__init__()
        self.title = 'Dashboard'
        self.content = 'Bem-vindo ao dashboard!'

    def render(self, q, zone=None, **kwargs):
        q.page['header'] = ui.markdown_card(
            box=zone or 'header',
            title=self.title,
            content=self.content
        )

# Card de formulário modular
class DashboardFormCard(BaseCard):
    def __init__(self):
        super().__init__()
        self.last_input = None
        self.zone = 'main'
        self.add_handler('submit', self.on_submit)

    def render(self, q, zone=None, **kwargs):
        items = [
            ui.textbox(name='input', label='Digite algo'),
            ui.button(name='submit', label='Enviar', primary=True),
        ]
        if self.last_input:
            items.append(ui.text(content=f'Você digitou: {self.last_input}'))
        q.page['main'] = ui.form_card(
            box=zone or self.zone,
            items=items
        )

    async def on_submit(self, q):
        self.last_input = q.args.get('input', '')
        return True
"""
DAZE Template - Dashboard Page
Página principal com visão geral dos dados
"""

from h2o_wave import Q, ui
from pages.base import BasePage
from components.stats import StatsComponent
from components.charts import ChartComponent
from components.tables import TableComponent
from core.debug import DebugManager


class DashboardPage(BasePage):
    """
    Página de Dashboard - visão geral dos dados
    Demonstra como uma página orquestra múltiplos cards
    """
    
    def __init__(self, app=None):
        super().__init__(
            route='dashboard',
            title='Dashboard',
            app=app,
            icon='📊'
        )
        self.description = 'Visão geral dos dados e métricas principais'
        # Cards modulares
        self.header_card = DashboardHeaderCard()
        self.form_card = DashboardFormCard()
        self.add_card(self.header_card, zone='header')
        self.add_card(self.form_card, zone='main')
        # Registro modular do handler da tabela
        self.register_handler('sales_table', self.handle_sales_table)
    
    def setup_layout(self, q):
        q.page['meta'] = ui.meta_card(
            box='',
            layouts=[
                ui.layout(
                    breakpoint='xs',
                    zones=[
                        ui.zone('header'),
                        ui.zone('main'),
                        ui.zone('footer'),
                    ]
                )
            ]
        )
    
    async def render(self, q: Q):
        """Renderiza o dashboard com cards específicos (modular)"""
        debug = DebugManager.get_instance()
        debug.log('[DashboardPage.render] chamado')
        self.setup_layout(q)
        self.render_cards(q)
        # Cards extras (mantidos para exemplo)
        self._create_overview_card(q)
        self._create_chart_card(q)
        self._create_table_card(q)
        await q.page.save()
    
    def _create_overview_card(self, q: Q):
        """Cria card de visão geral com estatísticas"""
        q.page['overview'] = ui.stat_list_card(
            box='sidebar',
            title='📊 Métricas Principais',
            items=[
                ui.stat(
                    label='Vendas Hoje',
                    value='R$ 45.230',
                    caption='↗️ +12% vs ontem',
                    icon='Money'
                ),
                ui.stat(
                    label='Produtos Ativos',
                    value='1.247',
                    caption='📦 Em estoque',
                    icon='Product'
                ),
                ui.stat(
                    label='Usuários Online',
                    value='89',
                    caption='👥 Conectados agora',
                    icon='People'
                )
            ]
        )
    
    def _create_chart_card(self, q: Q):
        """Cria card com gráfico principal"""
        # Dados de exemplo
        data = [
            ['Jan', 100, 120, 80],
            ['Feb', 120, 140, 90],
            ['Mar', 150, 110, 110],
            ['Apr', 180, 160, 130],
            ['Mai', 200, 180, 150]
        ]
        
        q.page['main_chart'] = ui.plot_card(
            box='main',
            title='📈 Vendas por Mês',
            data=data,
            axes=[
                ui.axis(label='Mês'),
                ui.axis(label='Valor (R$ mil)', side='left')
            ],
            plots=[
                ui.plot([
                    ui.mark(
                        coord='rect',
                        type='interval',
                        x='=0',
                        y='=1',
                        color='steelblue',
                        stroke_width=0
                    )
                ])
            ]
        )
    
    def _create_table_card(self, q: Q):
        """Cria card com tabela de dados recentes"""
        q.page['recent_sales'] = ui.form_card(
            box='footer',
            title='📋 Vendas Recentes',
            items=[
                ui.table(
                    name='sales_table',
                    columns=[
                        ui.table_column('product', 'Produto', width='200px'),
                        ui.table_column('value', 'Valor', width='100px'),
                        ui.table_column('date', 'Data', width='120px'),
                        ui.table_column('status', 'Status', width='100px')
                    ],
                    rows=[
                        ui.table_row(name='row1', cells=[
                            'Produto A', 'R$ 1.250', '28/08/2025', '✅ Pago'
                        ]),
                        ui.table_row(name='row2', cells=[
                            'Produto B', 'R$ 890', '28/08/2025', '⏳ Pendente'
                        ]),
                        ui.table_row(name='row3', cells=[
                            'Produto C', 'R$ 2.100', '27/08/2025', '✅ Pago'
                        ])
                    ],
                    height='200px'
                )
            ]
        )
    
    async def handle_sales_table(self, q: Q):
        debug = DebugManager.get_instance()
        args = q.args if isinstance(q.args, dict) else {}
        selected_rows = args.get('sales_table')
        debug.log(f'[DashboardPage] sales_table selecionado: {selected_rows}')
        # Aqui poderia atualizar outros cards baseado na seleção
        return True
