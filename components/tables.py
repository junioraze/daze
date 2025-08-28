"""
Componente de tabelas reutilizável.
"""

from typing import List, Dict, Any, Optional
from h2o_wave import ui, data

from .base import BaseComponent


class TableComponent(BaseComponent):
    """Componente para renderizar tabelas de dados"""
    
    def __init__(self):
        super().__init__('tables')
    
    def render(self, table_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza tabela básica"""
        box = kwargs.get('box', 'table')
        title = kwargs.get('title', 'Tabela de Dados')
        downloadable = kwargs.get('downloadable', False)
        searchable = kwargs.get('searchable', True)
        sortable = kwargs.get('sortable', True)
        
        if not table_data:
            return self.create_empty_card(box, 'Nenhum dado para exibir')
        
        # Obter colunas dos dados
        columns = list(table_data[0].keys())
        
        # Criar colunas da tabela
        table_columns = []
        for col in columns:
            table_columns.append(ui.table_column(
                name=col,
                label=col.replace('_', ' ').title(),
                sortable=sortable,
                searchable=searchable
            ))
        
        # Converter dados para formato Wave
        wave_data = data(
            fields=columns,
            rows=[[str(row[field]) for field in columns] for row in table_data],
            pack=True
        )
        
        return ui.form_card(
            box=box,
            items=[
                ui.table(
                    name='data_table',
                    columns=table_columns,
                    rows=wave_data,
                    downloadable=downloadable,
                    height='400px'
                )
            ]
        )
    
    def render_stats_table(self, table_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza tabela de estatísticas"""
        box = kwargs.get('box', 'table')
        title = kwargs.get('title', 'Estatísticas')
        
        if not table_data:
            return self.create_empty_card(box, 'Nenhuma estatística disponível')
        
        # Preparar itens da stat_table
        items = []
        for row in table_data:
            # Extrair valores (assumindo que a primeira coluna é o label)
            keys = list(row.keys())
            label_key = keys[0]
            value_keys = keys[1:]
            
            # Criar cores baseadas nos valores (opcional)
            colors = []
            for key in value_keys:
                value = row[key]
                if isinstance(value, (int, float)):
                    if value > 0:
                        colors.append('$green')
                    elif value < 0:
                        colors.append('$red')
                    else:
                        colors.append('$neutral')
                else:
                    colors.append('$neutral')
            
            items.append(
                ui.stat_table_item(
                    label=str(row[label_key]),
                    values=[str(row[key]) for key in value_keys],
                    colors=colors if colors else None
                )
            )
        
        return ui.stat_table_card(
            box=box,
            title=title,
            columns=['Item'] + [key.replace('_', ' ').title() for key in value_keys],
            items=items
        )
    
    def render_comparison_table(self, table_data: List[Dict[str, Any]] = None, 
                               comparison_column: str = None, **kwargs) -> ui.FormCard:
        """Renderiza tabela com comparação de valores"""
        box = kwargs.get('box', 'table')
        title = kwargs.get('title', 'Comparação')
        
        if not table_data or not comparison_column:
            return self.create_empty_card(box, 'Dados insuficientes para comparação')
        
        # Encontrar valores máximo e mínimo para comparação
        values = [row[comparison_column] for row in table_data if isinstance(row[comparison_column], (int, float))]
        if not values:
            return self.create_empty_card(box, 'Nenhum valor numérico encontrado')
        
        max_value = max(values)
        min_value = min(values)
        
        # Criar colunas
        columns = list(table_data[0].keys())
        table_columns = []
        
        for col in columns:
            # Adicionar formatação especial para coluna de comparação
            if col == comparison_column:
                table_columns.append(ui.table_column(
                    name=col,
                    label=col.replace('_', ' ').title(),
                    data_type='number',
                    cell_type=ui.progress_table_cell_type(
                        min=min_value,
                        max=max_value
                    )
                ))
            else:
                table_columns.append(ui.table_column(
                    name=col,
                    label=col.replace('_', ' ').title()
                ))
        
        # Converter dados
        wave_data = data(
            fields=columns,
            rows=[[row[field] for field in columns] for row in table_data],
            pack=True
        )
        
        return ui.form_card(
            box=box,
            items=[
                ui.table(
                    name='comparison_table',
                    columns=table_columns,
                    rows=wave_data,
                    height='400px'
                )
            ]
        )
    
    def render_interactive_table(self, table_data: List[Dict[str, Any]] = None, **kwargs) -> ui.FormCard:
        """Renderiza tabela interativa com filtros"""
        box = kwargs.get('box', 'table')
        title = kwargs.get('title', 'Tabela Interativa')
        
        if not table_data:
            return self.create_empty_card(box, 'Nenhum dado para exibir')
        
        columns = list(table_data[0].keys())
        
        # Criar filtros para cada coluna
        filter_items = []
        for col in columns[:3]:  # Limitar a 3 filtros para não sobrecarregar
            unique_values = list(set(str(row[col]) for row in table_data))[:10]  # Máximo 10 valores
            if len(unique_values) > 1:
                filter_items.append(
                    ui.dropdown(
                        name=f'filter_{col}',
                        label=f'Filtro {col.replace("_", " ").title()}',
                        choices=[ui.choice('all', 'Todos')] + 
                               [ui.choice(val, val) for val in unique_values],
                        value='all',
                        trigger=True
                    )
                )
        
        # Tabela
        table_columns = [
            ui.table_column(
                name=col,
                label=col.replace('_', ' ').title(),
                sortable=True
            ) for col in columns
        ]
        
        wave_data = data(
            fields=columns,
            rows=[[str(row[field]) for field in columns] for row in table_data],
            pack=True
        )
        
        items = []
        if filter_items:
            items.extend([
                ui.text_m('🔍 Filtros'),
                ui.inline(items=filter_items),
                ui.separator()
            ])
        
        items.append(
            ui.table(
                name='interactive_table',
                columns=table_columns,
                rows=wave_data,
                downloadable=True,
                height='400px'
            )
        )
        
        return ui.form_card(box=box, items=items)
