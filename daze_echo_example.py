# Exemplo DAZE WaveApp funcional e minimalista

from h2o_wave import main, Q, ui, app, on
from components.base import BaseComponent, BaseCard
from pages.base import BasePage
from core.app import WaveApp

# --- Component ---
class EchoComponent(BaseComponent):
    def render(self, q, state=None):
        q.page[self.component_id] = ui.form_card(
            box='1 1 2 2',
            items=[
                ui.text_l('Olá DAZE!'),
                ui.textbox(name='dummy', label='Campo dummy (para submit)', visible=True),
                ui.button(name='echo', label='Echo', primary=True)
            ]
        )
        # Renderiza feedback padronizado
        result = self.get_result(q, 'echo')
        if result:
            q.page['echo_result'] = ui.markdown_card(box='1 3 2 1', title='Resultado', content=result)

    def on_echo(self, q, state=None, args=None):
        dummy = args.get('dummy')
        print(f'[ECHO][COMPONENT] on_echo chamado! {dummy}')
        return f'Você clicou! {dummy}'

# --- Card ---
class EchoCard(BaseCard):
    def __init__(self, card_id):
        super().__init__(card_id)
        self.add_component('main', EchoComponent('main'))
    def render(self, q, state=None, **kwargs):
        for c in self.components.values():
            c.render(q, state=state)

# --- Page ---
class EchoPage(BasePage):
    def __init__(self, page_id):
        super().__init__(page_id, title='Echo Example')
        self.add_card('main', EchoCard('main'))
    def render(self, q, state=None):
        for c in self.cards.values():
            c.render(q, state=state)

# --- App ---


# --- App DAZE com integração @on já no core ---
app_daze = WaveApp()
app_daze.add_page('main', EchoPage('main'))
app_daze.register_wave_event('echo')

@app("/")
async def serve(q: Q):
    print('RAW ARGS:', q.args)
    args = app_daze.get_args(q)
    print('ARGS:', args)
    if args:
        q.client.last_event = args.copy() if hasattr(args, 'copy') else dict(args)
    await app_daze.handle_events(q, args=args)
    app_daze.render(q)
    await q.page.save()
