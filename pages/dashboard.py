"""
Página de dashboard principal.
"""

from typing import List
from h2o_wave import Q, ui
import random
from datetime import datetime, timedelta

from .base import BasePage
from components import StatsComponent, ChartComponent, TableComponent


class DashboardPage(BasePage):
    """Página principal do dashboard"""
    
    def __init__(self, app: 'WaveApp'):
        super().__init__(app, '#dashboard', 'Dashboard', 'BarChart4')
        
        # Componentes da página
        self.stats_component = StatsComponent()
        self.chart_component = ChartComponent()
        self.table_component = TableComponent()
    
    async def render(self, q: Q) -> None:
        """Renderiza a página de dashboard"""
        
        # Layout da página
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
                                    ui.zone('stats', size='120px'),
                                    ui.zone(
                                        'main',
                                        size='1',
                                        direction='row',
                                        zones=[
                                            ui.zone('charts', size='2'),
                                            ui.zone('table', size='1')
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
        
        # Gerar dados de exemplo
        stats_data = self._generate_stats_data()
        chart_data = self._generate_chart_data()
        table_data = self._generate_table_data()
        
        # Renderizar componentes
        self.add_card(q, 'stats', self.stats_component.render(stats_data))
        self.add_card(q, 'charts', self.chart_component.render(chart_data))
        self.add_card(q, 'data_table', self.table_component.render(table_data))
        
        # Botão de refresh
        self.add_card(q, 'refresh_btn', ui.form_card(
            box='stats',
            items=[
                ui.buttons([
                    ui.button(
                        name='refresh_dashboard',
                        label='Atualizar Dados',
                        icon='Refresh',
                        primary=True
                    )
                ], justify='end')
            ]
        ))
    
    def _generate_stats_data(self) -> List[dict]:
        """Gera dados de estatísticas de exemplo"""
        return [
            {
                'label': 'Vendas',
                'value': f'R$ {random.randint(50000, 150000):,}',
                'icon': 'Money',
                'change': random.randint(-20, 30),
                'trend': 'up' if random.choice([True, False]) else 'down'
            },
            {
                'label': 'Usuários',
                'value': f'{random.randint(1000, 5000):,}',
                'icon': 'People',
                'change': random.randint(-10, 25),
                'trend': 'up' if random.choice([True, False]) else 'down'
            },
            {
                'label': 'Pedidos',
                'value': f'{random.randint(100, 500):,}',
                'icon': 'ShoppingCart',
                'change': random.randint(-15, 40),
                'trend': 'up' if random.choice([True, False]) else 'down'
            },
            {
                'label': 'Conversão',
                'value': f'{random.uniform(2.5, 8.5):.1f}%',
                'icon': 'BarChart4',
                'change': random.randint(-5, 15),
                'trend': 'up' if random.choice([True, False]) else 'down'
            }
        ]
    
    def _generate_chart_data(self) -> List[dict]:
        """Gera dados de gráfico de exemplo"""
        base_date = datetime.now() - timedelta(days=30)
        data = []
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'vendas': random.randint(1000, 5000),
                'usuarios': random.randint(100, 800),
                'pedidos': random.randint(20, 150)
            })
        
        return data
    
    def _generate_table_data(self) -> List[dict]:
        """Gera dados de tabela de exemplo"""
        produtos = [
            'Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E',
            'Produto F', 'Produto G', 'Produto H', 'Produto I', 'Produto J'
        ]
        
        data = []
        for produto in produtos:
            data.append({
                'produto': produto,
                'vendas': random.randint(100, 1000),
                'receita': random.randint(5000, 50000),
                'status': random.choice(['Ativo', 'Inativo', 'Pendente'])
            })
        
        return data
