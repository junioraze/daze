"""
Gerenciador de autenticação modular.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from h2o_wave import Q, ui
import json
import os
import hashlib
from datetime import datetime

from .models import User
print(f"[DEBUG] User importado em manager.py: {User}")


class AuthProvider(ABC):
    """Interface base para provedores de autenticação"""
    
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Autentica um usuário"""
        pass
    
    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[User]:
        """Obtém um usuário pelo ID"""
        pass
    
    @abstractmethod
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Cria um novo usuário"""
        pass


class SimpleAuthProvider(AuthProvider):
    """Provedor de autenticação simples baseado em arquivo JSON"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self._users: Dict[str, User] = {}
        self._load_users()
    
    def _load_users(self) -> None:
        """Carrega usuários do arquivo"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_data in data.get('users', []):
                        user = User.from_dict(user_data)
                        self._users[user.id] = user
            except Exception as e:
                print(f"Erro ao carregar usuários: {e}")
        else:
            # Criar usuário admin padrão
            admin_user = User(
                id="admin",
                username="admin",
                email="admin@example.com",
                full_name="Administrador",
                is_admin=True
            )
            self._users[admin_user.id] = admin_user
            self._save_users()
    
    def _save_users(self) -> None:
        """Salva usuários no arquivo"""
        try:
            data = {
                'users': [user.to_dict() for user in self._users.values()]
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        print(f"[DEBUG] authenticate chamado com: username={username}, password={password}")
        # Para o exemplo, senha padrão é "admin" para admin
        if username == "admin" and password == "admin":
            user = self._users.get("admin")
            print(f"[DEBUG] user encontrado para admin: {user}")
            if user:
                user.last_login = datetime.now()
                self._save_users()
                print(f"[DEBUG] user retornado: {user}")
                return user
        # Buscar por username ou email
        for user in self._users.values():
            print(f"[DEBUG] checando user: {user}")
            if (user.username == username or user.email == username) and user.is_active:
                user.last_login = datetime.now()
                self._save_users()
                print(f"[DEBUG] user retornado por username/email: {user}")
                return user
        print("[DEBUG] Nenhum usuário autenticado")
        return None
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Obtém usuário pelo ID"""
        return self._users.get(user_id)
    
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Cria novo usuário"""
        user = User(**user_data)
        self._users[user.id] = user
        self._save_users()
        return user


class AuthManager:
    """Gerenciador de autenticação"""
    
    def __init__(self, provider: AuthProvider):
        self.provider = provider
    
    async def is_authenticated(self, q: Q) -> bool:
        """Verifica se o usuário está autenticado"""
        return hasattr(q.client, 'user') and q.client.user is not None
    
    async def get_current_user(self, q: Q) -> Optional[User]:
        """Retorna o usuário atual"""
        if hasattr(q.client, 'user'):
            return q.client.user
        return None
    
    async def login(self, q: Q, username: str, password: str) -> bool:
        """Realiza login do usuário"""
        user = await self.provider.authenticate(username, password)
        if user:
            q.client.user = user
            q.client.authenticated = True
            return True
        return False
    
    async def logout(self, q: Q) -> None:
        """Realiza logout do usuário"""
        if hasattr(q.client, 'user'):
            delattr(q.client, 'user')
        q.client.authenticated = False
    
    async def show_login_form(self, q: Q) -> None:
        """Exibe formulário de login"""
        # Layout simples para login
        q.page['meta'] = ui.meta_card(
            box='',
            theme='neon',
            layouts=[
                ui.layout(
                    breakpoint='xs',
                    zones=[
                        ui.zone('content', size='1')
                    ]
                )
            ]
        )
        
        # Verificar se há erro de login
        show_error = hasattr(q.client, 'login_error') and q.client.login_error
        
        items = [
            ui.text_xl('🔐 Login'),
            ui.separator()
        ]
        
        if show_error:
            items.append(
                ui.message_bar(
                    type='error',
                    text='Usuário ou senha incorretos!'
                )
            )
            q.client.login_error = False
        
        items.extend([
            ui.textbox(
                name='username',
                label='Usuário',
                placeholder='Digite seu usuário ou email',
                required=True
            ),
            ui.textbox(
                name='password',
                label='Senha',
                placeholder='Digite sua senha',
                password=True,
                required=True
            ),
            ui.buttons([
                ui.button(
                    name='login_submit',
                    label='Entrar',
                    primary=True,
                    icon='SignIn'
                )
            ], justify='center'),
            ui.separator(),
            ui.text_s('💡 **Dica:** Use admin/admin para entrar')
        ])
        
        q.page['login_form'] = ui.form_card(
            box='content',
            items=items
        )
