"""
Sistema de autenticação modular para aplicações Wave.
"""

from .manager import AuthManager, SimpleAuthProvider
from .models import User

__all__ = ['AuthManager', 'SimpleAuthProvider', 'User']
