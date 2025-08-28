"""
Componente de gráficos reutilizável.
"""

from typing import List, Dict, Any
from h2o_wave import ui, data

from .base import BaseComponent


class ChartComponent(BaseComponent):
    """Componente para renderizar diferentes tipos de gráficos"""
    
    def __init__(self):
        super().__init__('charts')
    
    def render(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico padrão (linha)"""
        return self.render_line_chart(chart_data, **kwargs)
    
    def render_line_chart(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico de linha"""
        box = kwargs.get('box', 'charts')
        title = kwargs.get('title', 'Gráfico de Linha')
        x_field = kwargs.get('x_field', 'date')
        y_field = kwargs.get('y_field', 'value')
        
        if not chart_data:
            return self.create_empty_card(box, 'Nenhum dado para o gráfico')
        
        # Converter dados para formato Wave
        wave_data = data(
            fields=list(chart_data[0].keys()),
            rows=[[row[field] for field in chart_data[0].keys()] for row in chart_data],
            pack=True
        )
        
        return ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=ui.plot([
                ui.mark(
                    type='line',
                    x=f'={x_field}',
                    y=f'={y_field}',
                    color='#1f77b4'
                )
            ])
        )
    
    def render_bar_chart(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico de barras"""
        box = kwargs.get('box', 'charts')
        title = kwargs.get('title', 'Gráfico de Barras')
        x_field = kwargs.get('x_field', 'category')
        y_field = kwargs.get('y_field', 'value')
        
        if not chart_data:
            return self.create_empty_card(box, 'Nenhum dado para o gráfico')
        
        wave_data = data(
            fields=list(chart_data[0].keys()),
            rows=[[row[field] for field in chart_data[0].keys()] for row in chart_data],
            pack=True
        )
        
        return ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=ui.plot([
                ui.mark(
                    type='interval',
                    x=f'={x_field}',
                    y=f'={y_field}',
                    color='#ff7f0e'
                )
            ])
        )
    
    def render_multi_line_chart(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico de múltiplas linhas"""
        box = kwargs.get('box', 'charts')
        title = kwargs.get('title', 'Gráfico Multi-linha')
        x_field = kwargs.get('x_field', 'date')
        y_fields = kwargs.get('y_fields', ['vendas', 'usuarios'])
        
        if not chart_data:
            return self.create_empty_card(box, 'Nenhum dado para o gráfico')
        
        wave_data = data(
            fields=list(chart_data[0].keys()),
            rows=[[row[field] for field in chart_data[0].keys()] for row in chart_data],
            pack=True
        )
        
        # Criar marks para cada série
        marks = []
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, y_field in enumerate(y_fields):
            marks.append(
                ui.mark(
                    type='line',
                    x=f'={x_field}',
                    y=f'={y_field}',
                    color=colors[i % len(colors)]
                )
            )
        
        return ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=ui.plot(marks)
        )
    
    def render_area_chart(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico de área"""
        box = kwargs.get('box', 'charts')
        title = kwargs.get('title', 'Gráfico de Área')
        x_field = kwargs.get('x_field', 'date')
        y_field = kwargs.get('y_field', 'value')
        
        if not chart_data:
            return self.create_empty_card(box, 'Nenhum dado para o gráfico')
        
        wave_data = data(
            fields=list(chart_data[0].keys()),
            rows=[[row[field] for field in chart_data[0].keys()] for row in chart_data],
            pack=True
        )
        
        return ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=ui.plot([
                ui.mark(
                    type='area',
                    x=f'={x_field}',
                    y=f'={y_field}',
                    color='#2ca02c',
                    fill_opacity=0.7
                )
            ])
        )
    
    def render_pie_chart(self, chart_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza gráfico de pizza"""
        box = kwargs.get('box', 'charts')
        title = kwargs.get('title', 'Gráfico de Pizza')
        category_field = kwargs.get('category_field', 'category')
        value_field = kwargs.get('value_field', 'value')
        
        if not chart_data:
            return self.create_empty_card(box, 'Nenhum dado para o gráfico')
        
        wave_data = data(
            fields=list(chart_data[0].keys()),
            rows=[[row[field] for field in chart_data[0].keys()] for row in chart_data],
            pack=True
        )
        
        return ui.plot_card(
            box=box,
            title=title,
            data=wave_data,
            plot=ui.plot([
                ui.mark(
                    type='arc',
                    theta=f'={value_field}',
                    color=f'={category_field}',
                    stroke_width=2
                )
            ])
        )
