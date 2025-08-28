"""
Página de análise avançada.
Exemplo de como estender a template com novas páginas.
"""

from typing import List
from h2o_wave import Q, ui
import random
import pandas as pd
from datetime import datetime, timedelta

from pages.base import BasePage
from components import ChartComponent, TableComponent


class AnalyticsPage(BasePage):
    """Página de análise avançada"""
    
    def __init__(self, app: 'WaveApp'):
        super().__init__(app, '#analytics', 'Analytics', 'LineChart')
        
        # Componentes específicos da página
        self.chart_component = ChartComponent()
        self.table_component = TableComponent()
    
    async def render(self, q: Q) -> None:
        """Renderiza a página de analytics"""
        
        # Layout específico para analytics
        q.page['meta'].layouts = [
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('header', size='80px'),
                    ui.zone(
                        'body',
                        size='1',
                        direction='row',
                        zones=[
                            ui.zone('sidebar', size='250px'),
                            ui.zone(
                                'content',
                                size='1',
                                direction='column',
                                zones=[
                                    ui.zone('controls', size='100px'),
                                    ui.zone(
                                        'analytics_main',
                                        size='1',
                                        direction='row',
                                        zones=[
                                            ui.zone('chart_area', size='2'),
                                            ui.zone('metrics', size='1')
                                        ]
                                    ),
                                    ui.zone('detailed_table', size='300px')
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
        
        # Cabeçalho da página
        self.add_card(q, 'page_header', ui.form_card(
            box='controls',
            items=[
                ui.inline([
                    ui.text_xl('📊 Analytics Avançado'),
                    ui.buttons([
                        ui.button('export_data', 'Exportar', icon='Download'),
                        ui.button('refresh_analytics', 'Atualizar', icon='Refresh', primary=True)
                    ])
                ])
            ]
        ))
        
        # Gerar dados de análise
        chart_data = self._generate_analytics_data()
        metrics_data = self._generate_metrics()
        detailed_data = self._generate_detailed_table()
        
        # Gráfico principal
        self.add_card(q, 'main_chart', ui.plot_card(
            box='chart_area',
            title='Tendências de Performance',
            data=chart_data,
            plot=ui.plot([
                ui.mark(
                    coord='rect',
                    type='line',
                    x='=date',
                    y='=revenue',
                    stroke_width=3,
                    color='$blue'
                ),
                ui.mark(
                    coord='rect',
                    type='line',
                    x='=date',
                    y='=users',
                    stroke_width=2,
                    color='$green',
                    y_field='users'
                )
            ]),
            axes=[
                ui.axis(label='Data', side='bottom'),
                ui.axis(label='Receita (R$)', side='left'),
                ui.axis(label='Usuários', side='right', color='$green')
            ]
        ))
        
        # Métricas laterais
        self.add_card(q, 'metrics_panel', ui.form_card(
            box='metrics',
            items=[
                ui.text_l('📈 Métricas Chave'),
                ui.separator(),
                *[
                    ui.stat(
                        label=metric['label'],
                        value=metric['value'],
                        icon=metric['icon'],
                        icon_color=metric['color']
                    )
                    for metric in metrics_data
                ],
                ui.separator(),
                ui.text_m('🎯 Insights'),
                ui.text_s('• Crescimento consistente de 15%'),
                ui.text_s('• Pico de usuários às quintas'),
                ui.text_s('• Conversão melhorou 8%'),
            ]
        ))
        
        # Tabela detalhada
        self.add_card(q, 'detailed_analytics', ui.table_card(
            box='detailed_table',
            title='📋 Dados Detalhados',
            data=detailed_data,
            columns=[
                ui.table_column('metric', 'Métrica', sortable=True),
                ui.table_column('current', 'Atual', data_type='number'),
                ui.table_column('previous', 'Anterior', data_type='number'),
                ui.table_column('change', 'Variação', data_type='number'),
                ui.table_column('trend', 'Tendência')
            ],
            height='250px'
        ))
    
    def _generate_analytics_data(self) -> List[List]:
        """Gera dados para o gráfico de analytics"""
        base_date = datetime.now() - timedelta(days=30)
        data = [['date', 'revenue', 'users']]
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            revenue = random.randint(10000, 50000)
            users = random.randint(500, 2000)
            data.append([
                date.strftime('%Y-%m-%d'),
                revenue,
                users
            ])
        
        return data
    
    def _generate_metrics(self) -> List[dict]:
        """Gera métricas para o painel lateral"""
        return [
            {
                'label': 'ROI',
                'value': f'{random.uniform(15, 35):.1f}%',
                'icon': 'TrendingUp',
                'color': '$green'
            },
            {
                'label': 'CAC',
                'value': f'R$ {random.randint(50, 200)}',
                'icon': 'Money',
                'color': '$blue'
            },
            {
                'label': 'LTV',
                'value': f'R$ {random.randint(500, 2000)}',
                'icon': 'Diamond',
                'color': '$purple'
            },
            {
                'label': 'Churn',
                'value': f'{random.uniform(2, 8):.1f}%',
                'icon': 'Warning',
                'color': '$orange'
            }
        ]
    
    def _generate_detailed_table(self) -> List[List]:
        """Gera dados para tabela detalhada"""
        metrics = [
            'Receita Total', 'Novos Usuários', 'Sessões',
            'Taxa de Conversão', 'Ticket Médio', 'Retenção'
        ]
        
        data = [['metric', 'current', 'previous', 'change', 'trend']]
        
        for metric in metrics:
            current = random.randint(1000, 10000)
            previous = random.randint(800, 9000)
            change = ((current - previous) / previous) * 100
            trend = '📈' if change > 0 else '📉'
            
            data.append([
                metric,
                current,
                previous,
                f'{change:+.1f}%',
                trend
            ])
        
        return data
