"""
DAZE Template - Pages Module
Páginas da aplicação Wave
"""

from .base import BasePage
from .dashboard import DashboardPage
from .sales import SalesPage
from .products import ProductsPage
from .reports import ReportsPage

__all__ = [
    'BasePage',
    'DashboardPage', 
    'SalesPage',
    'ProductsPage',
    'ReportsPage'
]
