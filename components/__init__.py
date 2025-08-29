"""
DAZE Template - Components Module
Componentes reutilizáveis da aplicação
"""

from .base import BaseComponent, BaseCard

# Imports condicionais para evitar erros
try:
    from .stats import StatsComponent
    from .charts import ChartComponent  
    from .tables import TableComponent
    from .header import HeaderComponent, BreadcrumbComponent
    __all__ = [
        'BaseComponent', 
        'BaseCard', 
        'StatsComponent', 
        'ChartComponent', 
        'TableComponent',
        'HeaderComponent',
        'BreadcrumbComponent'
    ]
except ImportError as e:
    print(f"Aviso: Erro ao importar alguns componentes: {e}")
    __all__ = ['BaseComponent', 'BaseCard']
