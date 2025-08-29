"""
DAZE Template - Charts Component
Componente para exibição de gráficos usando H2O Wave
"""

from h2o_wave import Q, ui
from .base import BaseComponent


class ChartComponent(BaseComponent):
    """
    Componente de gráficos reutilizável.
    Suporta diferentes tipos de gráficos (line, bar, area, etc.)
    """
    
    def __init__(self, component_id: str = 'chart'):
        super().__init__(component_id)
    
    async def create(self, q: Q, **kwargs):
        """Cria um gráfico baseado nos parâmetros fornecidos"""
        # Parâmetros padrão
        chart_type = kwargs.get('chart_type', 'line')
        data = kwargs.get('data', [])
        title = kwargs.get('title', 'Gráfico')
        box = kwargs.get('box', 'content')
        x_field = kwargs.get('x_field', 'x')
        y_field = kwargs.get('y_field', 'y')
        
        # Converte dados para formato Wave se necessário
        if data and isinstance(data[0], dict):
            wave_data = [[row[x_field], row[y_field]] for row in data if x_field in row and y_field in row]
        else:
            wave_data = data if data else [['Jan', 100], ['Feb', 150], ['Mar', 200]]
        
        # Cria o gráfico baseado no tipo
        if chart_type == 'line':
            chart = self._create_line_chart()
        elif chart_type == 'bar':
            chart = self._create_bar_chart()
        elif chart_type == 'area':
            chart = self._create_area_chart()
        else:
            chart = self._create_line_chart()
        
        q.page[self.component_id] = ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=chart
        )
    
    def _create_line_chart(self):
        """Cria um gráfico de linha"""
        return ui.plot([
            ui.mark(
                coord='rect',
                type='line',
                x='=0',
                y='=1',
                color='$blue'
            )
        ])
    
    def _create_bar_chart(self):
        """Cria um gráfico de barras"""
        return ui.plot([
            ui.mark(
                coord='rect',
                type='interval',
                x='=0',
                y='=1',
                color='$green'
            )
        ])
    
    def _create_area_chart(self):
        """Cria um gráfico de área"""
        return ui.plot([
            ui.mark(
                coord='rect',
                type='area',
                x='=0',
                y='=1',
                color='$orange'
            )
        ])
    
    async def update(self, q: Q, **kwargs):
        """Atualiza o gráfico com novos dados"""
        await self.create(q, **kwargs)