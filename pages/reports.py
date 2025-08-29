"""
DAZE Template - Reports Page
Página de relatórios customizados
"""

from h2o_wave import Q, ui
from pages.base import BasePage


class ReportsPage(BasePage):
    """
    Página de Relatórios - geração de relatórios customizados
    Demonstra geração dinâmica de conteúdo baseado em parâmetros
    """
    
    def __init__(self, app=None):
        super().__init__(
            route='reports',
            title='Relatórios',
            app=app,
            icon='📋'
        )
        self.description = 'Geração de relatórios customizados'
        self.data_service = app.data_service if app else None
    
    def setup_layout(self, q: Q, zones=None):
        """Layout específico da página de relatórios"""
        if not zones:
            zones = [
                ui.zone('header', size='60px'),
                ui.zone('breadcrumb', size='40px'),
                ui.zone('content', direction='row', zones=[
                    ui.zone('generator', size='35%'),
                    ui.zone('report', size='65%')
                ])
            ]
        
        q.page['meta'] = ui.meta_card(
            box='', 
            layouts=[ui.layout(breakpoint='xs', zones=zones)]
        )
    
    async def render(self, q: Q):
        """Renderiza a página de relatórios"""
        self.setup_layout(q)
        
        # Card gerador de relatórios
        self._create_generator_card(q)
        
        # Card do relatório
        await self._create_report_card(q)
        
        await q.page.save()
    
    def _create_generator_card(self, q: Q):
        """Cria card para configurar e gerar relatórios"""
        report_type = self.get_state(q, 'report_type', 'sales_summary')
        date_from = self.get_state(q, 'date_from', '2025-08-01')
        date_to = self.get_state(q, 'date_to', '2025-08-28')
        include_charts = self.get_state(q, 'include_charts', True)
        
        q.page['report_generator'] = ui.form_card(
            box='generator',
            title='📋 Gerador de Relatórios',
            items=[
                ui.separator('Tipo de Relatório'),
                ui.dropdown(
                    name='report_type',
                    label='Tipo',
                    value=report_type,
                    choices=[
                        ui.choice('sales_summary', '💰 Resumo de Vendas'),
                        ui.choice('product_analysis', '📦 Análise de Produtos'),
                        ui.choice('customer_report', '👥 Relatório de Clientes'),
                        ui.choice('financial_overview', '💹 Visão Financeira'),
                        ui.choice('custom_kpi', '📊 KPIs Customizados')
                    ]
                ),
                ui.separator('Período'),
                ui.date_picker(
                    name='date_from',
                    label='Data Inicial',
                    value=date_from
                ),
                ui.date_picker(
                    name='date_to',
                    label='Data Final',
                    value=date_to
                ),
                ui.separator('Opções'),
                ui.checkbox(
                    name='include_charts',
                    label='Incluir Gráficos',
                    value=include_charts
                ),
                ui.checkbox(
                    name='include_tables',
                    label='Incluir Tabelas Detalhadas',
                    value=self.get_state(q, 'include_tables', True)
                ),
                ui.checkbox(
                    name='include_summary',
                    label='Incluir Resumo Executivo',
                    value=self.get_state(q, 'include_summary', True)
                ),
                ui.separator('Ações'),
                ui.button(
                    name='generate_report',
                    label='📋 Gerar Relatório',
                    primary=True
                ),
                ui.button(
                    name='export_pdf',
                    label='📄 Exportar PDF'
                ),
                ui.button(
                    name='schedule_report',
                    label='⏰ Agendar'
                ),
                ui.separator('Relatórios Salvos'),
                ui.link(
                    name='saved_reports',
                    label='📁 Ver Relatórios Salvos',
                    path='#'
                ),
                ui.text(f'**Último gerado:** {self.get_state(q, "last_generated", "N/A")}')
            ]
        )
    
    async def _create_report_card(self, q: Q):
        """Cria card com o relatório gerado"""
        report_type = self.get_state(q, 'report_type', 'sales_summary')
        
        # Verifica se há relatório gerado
        if not self.get_state(q, 'report_generated', False):
            q.page['report_display'] = ui.form_card(
                box='report',
                title='📄 Relatório',
                items=[
                    ui.text('👈 **Configure os parâmetros e clique em "Gerar Relatório"**'),
                    ui.separator(),
                    ui.text('**Tipos de relatório disponíveis:**'),
                    ui.text('• 💰 **Resumo de Vendas** - Análise de performance de vendas'),
                    ui.text('• 📦 **Análise de Produtos** - Produtos mais vendidos e estoque'),
                    ui.text('• 👥 **Relatório de Clientes** - Segmentação e comportamento'),
                    ui.text('• 💹 **Visão Financeira** - Receitas, custos e margens'),
                    ui.text('• 📊 **KPIs Customizados** - Indicadores personalizados'),
                    ui.separator(),
                    ui.text('**Funcionalidades:**'),
                    ui.text('✅ Filtros por período'),
                    ui.text('✅ Gráficos interativos'),
                    ui.text('✅ Tabelas detalhadas'),
                    ui.text('✅ Exportação PDF'),
                    ui.text('✅ Agendamento automático')
                ]
            )
        else:
            # Gera o relatório baseado no tipo selecionado
            await self._generate_report_content(q, report_type)
    
    async def _generate_report_content(self, q: Q, report_type: str):
        """Gera conteúdo do relatório baseado no tipo"""
        date_from = self.get_state(q, 'date_from', '2025-08-01')
        date_to = self.get_state(q, 'date_to', '2025-08-28')
        include_charts = self.get_state(q, 'include_charts', True)
        
        report_titles = {
            'sales_summary': '💰 Relatório de Vendas',
            'product_analysis': '📦 Análise de Produtos',
            'customer_report': '👥 Relatório de Clientes',
            'financial_overview': '💹 Visão Financeira',
            'custom_kpi': '📊 KPIs Customizados'
        }
        
        title = report_titles.get(report_type, 'Relatório')
        
        try:
            # Busca dados do DataService se disponível
            if self.data_service:
                report_data = await self._fetch_report_data(report_type, date_from, date_to)
            else:
                report_data = self._get_fallback_report_data(report_type)
            
            # Cria itens do relatório
            report_items = [
                ui.text_xl(f'**{title}**'),
                ui.text(f'📅 Período: {date_from} até {date_to}'),
                ui.separator()
            ]
            
            # Adiciona resumo executivo
            if self.get_state(q, 'include_summary', True):
                report_items.extend(self._create_executive_summary(report_data, report_type))
            
            # Adiciona gráfico se solicitado
            if include_charts:
                report_items.extend(self._create_report_chart(report_data, report_type))
            
            # Adiciona tabela se solicitada
            if self.get_state(q, 'include_tables', True):
                report_items.extend(self._create_report_table(report_data, report_type))
            
            # Adiciona footer
            report_items.extend([
                ui.separator(),
                ui.text(f'📊 **Relatório gerado em:** {self.get_state(q, "last_generated", "28/08/2025 - 14:30")}'),
                ui.text('🌊 **Gerado por:** DAZE Template - H2O Wave')
            ])
            
            q.page['report_display'] = ui.form_card(
                box='report',
                title=title,
                items=report_items
            )
            
        except Exception as e:
            q.page['report_display'] = ui.form_card(
                box='report',
                title=f'{title} - Erro',
                items=[
                    ui.text(f'⚠️ Erro ao gerar relatório: {str(e)}'),
                    ui.button('retry_report', 'Tentar Novamente')
                ]
            )
    
    def _create_executive_summary(self, data, report_type):
        """Cria resumo executivo baseado no tipo de relatório"""
        summaries = {
            'sales_summary': [
                ui.text('**📈 Resumo Executivo**'),
                ui.text('• Vendas totais: R$ 125.430'),
                ui.text('• Crescimento: +12% vs período anterior'),
                ui.text('• Ticket médio: R$ 230'),
                ui.text('• Top produto: Notebook Dell (25% das vendas)'),
                ui.separator()
            ],
            'product_analysis': [
                ui.text('**📦 Resumo de Produtos**'),
                ui.text('• Total de produtos ativos: 1.247'),
                ui.text('• Produtos em baixo estoque: 23'),
                ui.text('• Categoria mais vendida: Eletrônicos'),
                ui.text('• Margem média: 35%'),
                ui.separator()
            ],
            'customer_report': [
                ui.text('**👥 Resumo de Clientes**'),
                ui.text('• Clientes ativos: 2.456'),
                ui.text('• Novos clientes: 89 (este mês)'),
                ui.text('• Taxa de retenção: 87%'),
                ui.text('• Segmento principal: Premium (40%)'),
                ui.separator()
            ]
        }
        
        return summaries.get(report_type, [ui.text('**Resumo não disponível**'), ui.separator()])
    
    def _create_report_chart(self, data, report_type):
        """Cria gráfico para o relatório"""
        chart_data = [
            ['Jan', 100], ['Feb', 120], ['Mar', 150], ['Apr', 180], ['Mai', 200]
        ]
        
        return [
            ui.text('**📊 Gráfico de Tendência**'),
            # Nota: Em um app real, usaria ui.plot_card ou ui.visualization
            ui.text('📈 [Gráfico seria renderizado aqui]'),
            ui.text('Dados: Crescimento constante de 20% ao mês'),
            ui.separator()
        ]
    
    def _create_report_table(self, data, report_type):
        """Cria tabela para o relatório"""
        return [
            ui.text('**📋 Dados Detalhados**'),
            ui.table(
                name='report_table',
                columns=[
                    ui.table_column('item', 'Item', width='200px'),
                    ui.table_column('value', 'Valor', width='100px'),
                    ui.table_column('change', 'Variação', width='100px')
                ],
                rows=[
                    ui.table_row('r1', ['Vendas Totais', 'R$ 125.430', '+12%']),
                    ui.table_row('r2', ['Produtos Vendidos', '542 unid.', '+8%']),
                    ui.table_row('r3', ['Ticket Médio', 'R$ 230', '+3%'])
                ],
                height='200px'
            )
        ]
    
    async def _fetch_report_data(self, report_type, date_from, date_to):
        """Busca dados do DataService para o relatório"""
        # Implementação simplificada
        return {'type': report_type, 'period': f'{date_from} to {date_to}'}
    
    def _get_fallback_report_data(self, report_type):
        """Dados de fallback para relatórios"""
        return {'type': report_type, 'sample': True}
    
    async def handle_events(self, q: Q):
        """Processa eventos específicos da página de relatórios"""
        if q.args.generate_report:
            # Salva parâmetros e gera relatório
            if q.args.report_type:
                self.set_state(q, 'report_type', q.args.report_type)
            if q.args.date_from:
                self.set_state(q, 'date_from', q.args.date_from)
            if q.args.date_to:
                self.set_state(q, 'date_to', q.args.date_to)
            if q.args.include_charts is not None:
                self.set_state(q, 'include_charts', q.args.include_charts)
            if q.args.include_tables is not None:
                self.set_state(q, 'include_tables', q.args.include_tables)
            if q.args.include_summary is not None:
                self.set_state(q, 'include_summary', q.args.include_summary)
            
            # Marca como gerado e atualiza timestamp
            self.set_state(q, 'report_generated', True)
            self.set_state(q, 'last_generated', '28/08/2025 - 14:30')
            
            # Re-renderiza com o relatório
            await self._create_report_card(q)
            self._create_generator_card(q)  # Atualiza timestamp
            
            await q.page.save()
            return True
        
        elif q.args.export_pdf:
            # Simula exportação PDF
            # Em um app real, geraria e baixaria o PDF
            q.page['pdf_export'] = ui.form_card(
                box='report',
                title='📄 Exportação PDF',
                items=[
                    ui.text('✅ **Relatório exportado com sucesso!**'),
                    ui.text('📁 Arquivo: relatorio_vendas_28082025.pdf'),
                    ui.text('📍 Local: Downloads/Relatorios/'),
                    ui.button('close_export', 'Fechar')
                ]
            )
            await q.page.save()
            return True
        
        elif q.args.close_export:
            await self._create_report_card(q)
            await q.page.save()
            return True
        
        elif q.args.retry_report:
            await self._create_report_card(q)
            await q.page.save()
            return True
        
        # Chama o handler base
        return await super().handle_events(q)
