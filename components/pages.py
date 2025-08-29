"""
Páginas específicas para demonstrar funcionalidades do DAZE
"""
from h2o_wave import ui, Q
from .base import BaseCard
from .charts import ChartComponent
from .stats import StatsComponent  
from .tables import TableComponent
from services.data_service import DataService


class DashboardPage(BaseCard):
    """Página principal - Dashboard geral"""
    
    def __init__(self, card_id: str = "dashboard_page"):
        super().__init__(card_id)
        self.stats = StatsComponent('dashboard_stats')
        self.chart = ChartComponent('dashboard_chart')
        self.data_service = DataService()
    
    async def create(self, q: Q, **kwargs) -> None:
        """Cria a página de dashboard"""
        try:
            # Dados resumidos
            sales_data = await self.data_service.get_sample_sales_data(days=30)
            product_data = await self.data_service.get_sample_product_data(count=10)
            
            # Estatísticas gerais
            total_sales = sum([item['value'] for item in sales_data])
            avg_daily = total_sales / 30
            total_products = len(product_data)
            
            # Stats card
            await self.stats.create(q,
                title="📊 Resumo Geral - 30 dias",
                metrics=[
                    {'label': 'Vendas Total', 'value': f'${total_sales:,.2f}', 'delta': '+12.5%'},
                    {'label': 'Média Diária', 'value': f'${avg_daily:,.2f}', 'delta': '+8.3%'},
                    {'label': 'Produtos Ativos', 'value': str(total_products), 'delta': '+2'},
                    {'label': 'Conversão', 'value': '3.4%', 'delta': '+0.8%'}
                ]
            )
            
            # Chart card
            await self.chart.create(q,
                title="📈 Vendas dos Últimos 30 Dias",
                chart_data=sales_data,
                chart_type='line'
            )
            
            # Quick actions
            q.page[f'{self.card_id}_actions'] = ui.form_card(
                box='actions',
                title='🚀 Ações Rápidas',
                items=[
                    ui.text('**Navegue para páginas específicas:**'),
                    ui.buttons([
                        ui.button('nav_sales', '💰 Analisar Vendas', primary=True),
                        ui.button('nav_products', '📦 Filtrar Produtos'),
                    ]),
                    ui.buttons([
                        ui.button('nav_reports', '📋 Gerar Relatórios'),
                        ui.button('nav_analytics', '📈 Analytics Avançado')
                    ]),
                ]
            )
            
        except Exception as e:
            await self._handle_error(q, f"Erro no Dashboard: {str(e)}")


class SalesPage(BaseCard):
    """Página de análise de vendas"""
    
    def __init__(self, card_id: str = "sales_page"):
        super().__init__(card_id)
        self.chart = ChartComponent('sales_chart')
        self.stats = StatsComponent('sales_stats')
        self.data_service = DataService()
    
    async def create(self, q: Q, **kwargs) -> None:
        """Cria a página de vendas"""
        days = kwargs.get('days', 7)
        
        try:
            # Controles de filtro
            q.page[f'{self.card_id}_controls'] = ui.form_card(
                box='controls',
                title='🎛️ Filtros de Vendas',
                items=[
                    ui.text('**Configure o período de análise:**'),
                    ui.spinbox('sales_days', label='Período (dias)', value=days, min=1, max=90),
                    ui.dropdown('sales_metric', label='Métrica', value='revenue', choices=[
                        ui.choice('revenue', 'Receita'),
                        ui.choice('quantity', 'Quantidade'),
                        ui.choice('profit', 'Lucro')
                    ]),
                    ui.button('apply_sales_filter', '🔍 Aplicar Filtros', primary=True)
                ]
            )
            
            # Dados de vendas
            sales_data = await self.data_service.get_sample_sales_data(days=days)
            
            # Cálculos
            total_sales = sum([item['value'] for item in sales_data])
            avg_sale = total_sales / len(sales_data) if sales_data else 0
            
            # Stats
            await self.stats.create(q,
                title=f"📊 Vendas - {days} dias",
                metrics=[
                    {'label': 'Total', 'value': f'${total_sales:,.2f}', 'delta': '+15.2%'},
                    {'label': 'Média', 'value': f'${avg_sale:,.2f}', 'delta': '+5.1%'},
                    {'label': 'Transações', 'value': str(len(sales_data)), 'delta': '+23'},
                    {'label': 'Ticket Médio', 'value': f'${avg_sale * 1.2:,.2f}', 'delta': '+7.8%'}
                ]
            )
            
            # Chart
            await self.chart.create(q,
                title=f"📈 Evolução de Vendas - {days} dias",
                chart_data=sales_data,
                chart_type='area'
            )
            
        except Exception as e:
            await self._handle_error(q, f"Erro na página de Vendas: {str(e)}")


class ProductsPage(BaseCard):
    """Página de gestão de produtos"""
    
    def __init__(self, card_id: str = "products_page"):
        super().__init__(card_id)
        self.table = TableComponent('products_table')
        self.stats = StatsComponent('products_stats')
        self.data_service = DataService()
    
    async def create(self, q: Q, **kwargs) -> None:
        """Cria a página de produtos"""
        category = kwargs.get('category', 'all')
        count = kwargs.get('count', 15)
        
        try:
            # Controles
            q.page[f'{self.card_id}_controls'] = ui.form_card(
                box='controls',
                title='🎛️ Filtros de Produtos',
                items=[
                    ui.text('**Filtrar produtos por categoria:**'),
                    ui.dropdown('product_category', label='Categoria', value=category, choices=[
                        ui.choice('all', 'Todas'),
                        ui.choice('electronics', 'Eletrônicos'),
                        ui.choice('clothing', 'Roupas'),
                        ui.choice('home', 'Casa'),
                        ui.choice('sports', 'Esportes')
                    ]),
                    ui.spinbox('product_count', label='Quantidade', value=count, min=5, max=50),
                    ui.button('apply_product_filter', '🔍 Filtrar Produtos', primary=True)
                ]
            )
            
            # Dados
            product_data = await self.data_service.get_sample_product_data(count=count)
            
            # Stats
            total_value = sum([p.get('price', 0) for p in product_data])
            avg_price = total_value / len(product_data) if product_data else 0
            
            await self.stats.create(q,
                title=f"📦 Produtos - {category.title()}",
                metrics=[
                    {'label': 'Total Produtos', 'value': str(len(product_data)), 'delta': '+5'},
                    {'label': 'Valor Total', 'value': f'${total_value:,.2f}', 'delta': '+12%'},
                    {'label': 'Preço Médio', 'value': f'${avg_price:,.2f}', 'delta': '+3%'},
                    {'label': 'Categoria', 'value': category.title(), 'delta': ''}
                ]
            )
            
            # Tabela
            await self.table.create(q,
                title=f"📋 Lista de Produtos - {category.title()}",
                table_data=product_data,
                columns=['name', 'category', 'price', 'stock']
            )
            
        except Exception as e:
            await self._handle_error(q, f"Erro na página de Produtos: {str(e)}")


class ReportsPage(BaseCard):
    """Página de relatórios customizados"""
    
    def __init__(self, card_id: str = "reports_page"):
        super().__init__(card_id)
        self.table = TableComponent('reports_table')
        self.chart = ChartComponent('reports_chart')
        self.data_service = DataService()
    
    async def create(self, q: Q, **kwargs) -> None:
        """Cria a página de relatórios"""
        report_type = kwargs.get('report_type', 'sales')
        user_count = kwargs.get('user_count', 10)
        
        try:
            # Controles
            q.page[f'{self.card_id}_controls'] = ui.form_card(
                box='controls',
                title='📋 Gerador de Relatórios',
                items=[
                    ui.text('**Configure seu relatório personalizado:**'),
                    ui.dropdown('report_type', label='Tipo de Relatório', value=report_type, choices=[
                        ui.choice('sales', 'Relatório de Vendas'),
                        ui.choice('users', 'Relatório de Usuários'),
                        ui.choice('products', 'Relatório de Produtos'),
                        ui.choice('performance', 'Relatório de Performance')
                    ]),
                    ui.spinbox('report_count', label='Registros', value=user_count, min=5, max=100),
                    ui.button('generate_custom_report', '📊 Gerar Relatório', primary=True)
                ]
            )
            
            # Gera dados baseado no tipo
            if report_type == 'users':
                data = await self.data_service.get_sample_user_data(count=user_count)
                await self.table.create(q,
                    title=f"👥 Relatório de Usuários ({user_count} registros)",
                    table_data=data,
                    columns=['name', 'email', 'role', 'last_login']
                )
            else:
                # Relatório de vendas padrão
                sales_data = await self.data_service.get_sample_sales_data(days=30)
                await self.chart.create(q,
                    title=f"📈 Relatório de {report_type.title()}",
                    chart_data=sales_data,
                    chart_type='column'
                )
            
        except Exception as e:
            await self._handle_error(q, f"Erro na página de Relatórios: {str(e)}")


class AnalyticsPage(BaseCard):
    """Página de analytics avançado"""
    
    def __init__(self, card_id: str = "analytics_page"):
        super().__init__(card_id)
        self.chart1 = ChartComponent('analytics_chart1')
        self.chart2 = ChartComponent('analytics_chart2')
        self.stats = StatsComponent('analytics_stats')
        self.data_service = DataService()
    
    async def create(self, q: Q, **kwargs) -> None:
        """Cria a página de analytics"""
        try:
            # Controles
            q.page[f'{self.card_id}_controls'] = ui.form_card(
                box='controls',
                title='📈 Analytics Avançado',
                items=[
                    ui.text('**Análises comparativas e tendências:**'),
                    ui.dropdown('analytics_period', label='Período', value='month', choices=[
                        ui.choice('week', 'Última Semana'),
                        ui.choice('month', 'Último Mês'),
                        ui.choice('quarter', 'Último Trimestre'),
                        ui.choice('year', 'Último Ano')
                    ]),
                    ui.button('refresh_analytics', '🔄 Atualizar Analytics', primary=True)
                ]
            )
            
            # Dados para diferentes análises
            sales_data = await self.data_service.get_sample_sales_data(days=30)
            product_data = await self.data_service.get_sample_product_data(count=20)
            
            # Stats avançados
            await self.stats.create(q,
                title="📊 KPIs Avançados",
                metrics=[
                    {'label': 'ROI', 'value': '24.5%', 'delta': '+3.2%'},
                    {'label': 'Churn Rate', 'value': '2.1%', 'delta': '-0.5%'},
                    {'label': 'LTV', 'value': '$1,250', 'delta': '+15%'},
                    {'label': 'CAC', 'value': '$45', 'delta': '-8%'}
                ]
            )
            
            # Charts comparativos
            await self.chart1.create(q,
                title="📈 Tendência de Crescimento",
                chart_data=sales_data,
                chart_type='area'
            )
            
            # Simula dados de produtos para pie chart
            product_chart_data = [
                {'category': 'Electronics', 'value': 45},
                {'category': 'Clothing', 'value': 30},
                {'category': 'Home', 'value': 15},
                {'category': 'Sports', 'value': 10}
            ]
            
            await self.chart2.create(q,
                title="🥧 Distribuição por Categoria",
                chart_data=product_chart_data,
                chart_type='pie'
            )
            
        except Exception as e:
            await self._handle_error(q, f"Erro na página de Analytics: {str(e)}")
