"""
Modelos de dados para autenticação.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class User:
    """Modelo de usuário"""
    id: str
    username: str
    email: str
    full_name: str = ""
    is_active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o usuário para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Cria usuário a partir de dicionário"""
        print(f"[DEBUG] User.from_dict chamado com: {data}")
        user_data = data.copy()
        # Fallback para campos obrigatórios
        user_data.setdefault('id', '')
        user_data.setdefault('username', '')
        user_data.setdefault('email', '')
        user_data.setdefault('full_name', '')
        user_data.setdefault('is_active', True)
        user_data.setdefault('is_admin', False)
        user_data.setdefault('metadata', {})
        # Converter datas
        if user_data.get('created_at'):
            user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
        if user_data.get('last_login'):
            user_data['last_login'] = datetime.fromisoformat(user_data['last_login'])
        return cls(**user_data)
