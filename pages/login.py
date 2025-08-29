"""
Página de Login DAZE - Modular, herda BasePage
"""
from h2o_wave import Q, ui
from pages.base import BasePage
from core.debug import DebugManager

class LoginPage(BasePage):
    def __init__(self, app=None):
        super().__init__(route='login', title='Login', app=app, icon='Lock')
        # Registro modular do handler do botão do_login
        self.register_handler('do_login', self.handle_do_login)

    async def render(self, q: Q):
        debug = DebugManager.get_instance()
        debug.log(f'[LoginPage.render] chamado, callable={callable(self.render)}')
        self.setup_layout(q)
        q.page['login'] = ui.form_card(
            box='content',
            title='Login',
            items=[
                ui.textbox('username', label='Usuário'),
                ui.textbox('password', label='Senha', password=True),
                ui.button('do_login', 'Entrar', primary=True),
                ui.textbox('login_hidden', value='1', visible=False)
            ]
        )
        await q.page.save()

    async def handle_do_login(self, q: Q):
        debug = DebugManager.get_instance()
        args = q.args if isinstance(q.args, dict) else {}
        debug.log(f'[LoginPage.handle_do_login] chamado: args={args}')
        username = args.get('username')
        password = args.get('password')
        debug.log(f'[LoginPage] Tentando autenticar: username={username}')
        user = await self.app.auth_manager.authenticate(username, password)
        debug.log(f'[LoginPage] Resultado authenticate: {user}')
        if user:
            debug.log('[LoginPage] Autenticação bem-sucedida, redirecionando para dashboard')
            self.app.state_manager.set_client_state(q, 'user', user.to_dict())
            self.app.current_page = 'dashboard'
            debug.log(f'[LoginPage] current_page set para dashboard, user salvo em state_manager')
            return True
        else:
            debug.log('[LoginPage] Autenticação falhou, renderizando erro')
            q.page['login'] = ui.form_card(
                box='content',
                title='Login',
                items=[
                    ui.textbox('username', label='Usuário'),
                    ui.textbox('password', label='Senha', password=True),
                    ui.button('do_login', 'Entrar', primary=True),
                    ui.text('Usuário ou senha inválidos.')
                ]
            )
            await q.page.save()
            return True
