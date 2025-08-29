"""
DAZE Template - Sales Page
Página de análise de vendas com filtros dinâmicos
"""

from h2o_wave import Q, ui
from pages.base import BasePage


class SalesPage(BasePage):
    """
    Página de Vendas - análise detalhada com filtros
    Demonstra integração com DataService e parâmetros dinâmicos
    """
    
    def __init__(self, app=None):
        super().__init__(
            route='sales',
            title='Vendas',
            app=app,
            icon='💰'
        )
        self.description = 'Análise detalhada de vendas por período'
        self.data_service = app.data_service if app else None
    
    def setup_layout(self, q: Q, zones=None):
        """Layout específico da página de vendas"""
        if not zones:
            zones = [
                ui.zone('header', size='60px'),
                ui.zone('breadcrumb', size='40px'),
                ui.zone('content', direction='row', zones=[
                    ui.zone('filters', size='25%'),
                    ui.zone('main', size='75%', direction='column', zones=[
                        ui.zone('chart', size='60%'),
                        ui.zone('table', size='40%')
                    ])
                ])
            ]
        
        q.page['meta'] = ui.meta_card(
            box='', 
            layouts=[ui.layout(breakpoint='xs', zones=zones)]
        )
    
    async def render(self, q: Q):
        """Renderiza a página de vendas"""
        self.setup_layout(q)
        
        # Card de filtros
        self._create_filters_card(q)
        
        # Card de gráfico
        await self._create_chart_card(q)
        
        # Card de tabela
        await self._create_table_card(q)
        
        await q.page.save()
    
    def _create_filters_card(self, q: Q):
        """Cria card de filtros para análise de vendas"""
        # Valores atuais dos filtros
        days = self.get_state(q, 'days_filter', 30)
        period = self.get_state(q, 'period_filter', 'daily')
        
        q.page['sales_filters'] = ui.form_card(
            box='filters',
            title='🔍 Filtros de Vendas',
            items=[
                ui.separator('Período de Análise'),
                ui.spinbox(
                    name='days_filter',
                    label='Últimos Dias',
                    value=days,
                    min=1,
                    max=365,
                    step=1
                ),
                ui.dropdown(
                    name='period_filter',
                    label='Agrupamento',
                    value=period,
                    choices=[
                        ui.choice('daily', 'Diário'),
                        ui.choice('weekly', 'Semanal'),
                        ui.choice('monthly', 'Mensal')
                    ]
                ),
                ui.separator('Ações'),
                ui.button(
                    name='apply_sales_filters',
                    label='📊 Aplicar Filtros',
                    primary=True
                ),
                ui.button(
                    name='reset_sales_filters',
                    label='🔄 Limpar Filtros'
                ),
                ui.separator('Informações'),
                ui.text(f'**Período:** {days} dias'),
                ui.text(f'**Agrupamento:** {period}'),
                ui.text(f'**Última atualização:** {self.get_state(q, "last_update", "N/A")}')
            ]
        )
    
    async def _create_chart_card(self, q: Q):
        """Cria card com gráfico de vendas"""
        # Busca dados do DataService com filtros aplicados
        days = self.get_state(q, 'days_filter', 30)
        period = self.get_state(q, 'period_filter', 'daily')
        
        try:
            if self.data_service:
                sales_data = await self.data_service.get_sample_sales_data(days=days)
                # Processa dados baseado no período
                chart_data = self._process_sales_data(sales_data, period)
            else:
                # Dados de fallback
                chart_data = [
                    ['01/08', 1250],
                    ['02/08', 1890],
                    ['03/08', 2100],
                    ['04/08', 1750],
                    ['05/08', 2300]
                ]
            
            q.page['sales_chart'] = ui.plot_card(
                box='chart',
                title=f'💰 Vendas - Últimos {days} dias ({period})',
                data=chart_data,
                axes=[
                    ui.axis(label='Período'),
                    ui.axis(label='Vendas (R$)', side='left')
                ],
                plots=[
                    ui.plot([
                        ui.mark(
                            coord='rect',
                            type='line',
                            x='=0',
                            y='=1',
                            color='green',
                            stroke_width=2
                        )
                    ])
                ]
            )
            
        except Exception as e:
            q.page['sales_chart'] = ui.form_card(
                box='chart',
                title='💰 Vendas - Erro',
                items=[
                    ui.text(f'⚠️ Erro ao carregar dados: {str(e)}'),
                    ui.button('retry_sales_chart', 'Tentar Novamente')
                ]
            )
    
    async def _create_table_card(self, q: Q):
        """Cria card com tabela detalhada de vendas"""
        days = self.get_state(q, 'days_filter', 30)
        
        try:
            if self.data_service:
                sales_data = await self.data_service.get_sample_sales_data(days=days)
                table_rows = self._create_table_rows(sales_data)
            else:
                # Dados de fallback
                table_rows = [
                    ui.table_row('row1', ['Produto A', 'R$ 1.250', '28/08/2025', 'Cliente X']),
                    ui.table_row('row2', ['Produto B', 'R$ 890', '27/08/2025', 'Cliente Y']),
                    ui.table_row('row3', ['Produto C', 'R$ 2.100', '26/08/2025', 'Cliente Z'])
                ]
            
            q.page['sales_table'] = ui.form_card(
                box='table',
                title=f'📋 Detalhes de Vendas - Últimos {days} dias',
                items=[
                    ui.table(
                        name='sales_detail_table',
                        columns=[
                            ui.table_column('product', 'Produto', width='200px'),
                            ui.table_column('value', 'Valor', width='120px'),
                            ui.table_column('date', 'Data', width='120px'),
                            ui.table_column('client', 'Cliente', width='150px')
                        ],
                        rows=table_rows,
                        height='300px'
                    )
                ]
            )
            
        except Exception as e:
            q.page['sales_table'] = ui.form_card(
                box='table',
                title='📋 Detalhes de Vendas - Erro',
                items=[
                    ui.text(f'⚠️ Erro ao carregar dados: {str(e)}'),
                    ui.button('retry_sales_table', 'Tentar Novamente')
                ]
            )
    
    def _process_sales_data(self, raw_data, period):
        """Processa dados de vendas baseado no período selecionado"""
        # Implementação simplificada - em um caso real seria mais complexa
        if period == 'weekly':
            # Agrupa por semana
            return [['Semana 1', 5000], ['Semana 2', 7500], ['Semana 3', 6200], ['Semana 4', 8100]]
        elif period == 'monthly':
            # Agrupa por mês
            return [['Janeiro', 15000], ['Fevereiro', 18000], ['Março', 22000], ['Abril', 19500]]
        else:
            # Diário (padrão)
            return raw_data or [['Hoje', 2500], ['Ontem', 1900], ['Anteontem', 2100]]
    
    def _create_table_rows(self, sales_data):
        """Cria linhas da tabela baseado nos dados de vendas"""
        # Implementação simplificada
        rows = []
        for i, (date, value) in enumerate(sales_data or []):
            rows.append(ui.table_row(
                f'row_{i}',
                [f'Produto {i+1}', f'R$ {value}', date, f'Cliente {i+1}']
            ))
        return rows
    
    async def handle_events(self, q: Q):
        """Processa eventos específicos da página de vendas"""
        if q.args.apply_sales_filters:
            # Aplica filtros e atualiza dados
            if q.args.days_filter:
                self.set_state(q, 'days_filter', int(q.args.days_filter))
            if q.args.period_filter:
                self.set_state(q, 'period_filter', q.args.period_filter)
            
            self.set_state(q, 'last_update', '28/08/2025 - 14:30')
            
            # Re-renderiza cards com novos filtros
            await self._create_chart_card(q)
            await self._create_table_card(q)
            self._create_filters_card(q)  # Atualiza informações dos filtros
            
            await q.page.save()
            return True
        
        elif q.args.reset_sales_filters:
            # Reseta filtros para valores padrão
            self.set_state(q, 'days_filter', 30)
            self.set_state(q, 'period_filter', 'daily')
            self.set_state(q, 'last_update', 'Filtros resetados')
            
            # Re-renderiza com valores padrão
            await self._create_chart_card(q)
            await self._create_table_card(q)
            self._create_filters_card(q)
            
            await q.page.save()
            return True
        
        # Outros eventos...
        elif q.args.retry_sales_chart or q.args.retry_sales_table:
            await self._create_chart_card(q)
            await self._create_table_card(q)
            await q.page.save()
            return True
        
        # Chama o handler base
        return await super().handle_events(q)
