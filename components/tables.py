"""
Componente de tabelas reutilizável.
"""

from typing import List, Dict, Any
from h2o_wave import ui

from .base import BaseComponent


class TableComponent(BaseComponent):
    """Componente para exibir tabelas com dados dinâmicos"""
    
    def __init__(self, component_id: str):
        super().__init__(component_id)
    
    def create(self, q, table_data: List[Dict[str, Any]] = None, 
               box: str = 'content', title: str = 'Tabela', **kwargs):
        """Cria o componente de tabela na página Wave"""
        if not table_data:
            table_data = [{'coluna1': 'Sem dados', 'coluna2': 'Sem dados'}]
        
        # Extrair colunas dos dados
        columns = [ui.table_column(name=col, label=col.title()) 
                  for col in table_data[0].keys()]
        
        # Criar linhas
        rows = [ui.table_row(name=f'row_{i}', cells=[str(row[col]) for col in table_data[0].keys()]) 
                for i, row in enumerate(table_data)]
        
        q.page[self.component_id] = ui.form_card(
            box=box,
            title=title,
            items=[ui.table(name=f'{self.component_id}_table', columns=columns, rows=rows)]
        )
    
    def update(self, q, **kwargs):
        """Atualiza a tabela com novos dados"""
        # Re-criar com os novos dados
        self.create(q, **kwargs)
