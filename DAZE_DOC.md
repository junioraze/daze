# DAZE Template - Guia de Arquitetura, Uso e Conceito

## Visão Geral
O DAZE é um template modular para aplicações H2O Wave, focado em robustez, desacoplamento e facilidade de extensão. Ele padroniza o ciclo de eventos, extração de argumentos, fallback de estado e integração plugável com o decorador @on do Wave, permitindo criar aplicações Wave limpas, escaláveis e testáveis.

## Conceitos-Chave
- **Ciclo Modular:** App → Page → Card → Component, cada um responsável por sua lógica e propagação de eventos.
- **Extração Robusta de Args:** Sempre usa `WaveApp.get_args(q)`, que normaliza Expando, dict e __kv.
- **Fallback de Evento:** Se não houver args, busca o último evento em `q.client.last_event`.
- **Integração com @on:** O core DAZE permite registrar handlers @on(evento) plugáveis, sem duplicar lógica.
- **Handlers Plugáveis:** Cada nível pode registrar handlers para eventos específicos, mantendo o código limpo.

## Como Usar
### 1. Estrutura Básica
- Crie componentes herdando de `BaseComponent`, cards de `BaseCard`, páginas de `BasePage`.
- Implemente apenas lógica de negócio nos métodos `render` e `handle_events`.
- Não se preocupe com extração de args ou fallback: o core faz isso para você.

### 2. Integração com @on
- No app principal, use `app_daze.register_wave_event('nome_do_evento')` para criar handlers @on plugáveis.
- O ciclo de eventos é sempre o mesmo, seja via @on ou @app.


### 3. Exemplo Mínimo
```python
from h2o_wave import app, Q
from core.app import WaveApp
from pages.base import BasePage
from components.base import BaseComponent, BaseCard

class MyComponent(BaseComponent):
    def render(self, q, state=None):
        q.page[self.component_id] = ui.form_card(
            box='1 1 2 2',
            items=[
                ui.text_l('Exemplo DAZE!'),
                ui.textbox(name='dummy', label='Digite algo', visible=True),
                ui.button(name='meu_evento', label='Enviar', primary=True)
            ]
        )
        result = self.get_result(q, 'meu_evento')
        if result:
            q.page['result'] = ui.markdown_card(box='1 3 2 1', title='Resultado', content=result)

    def on_meu_evento(self, q, state=None, args=None):
        valor = args.get('dummy')
        return f'Você digitou: {valor}'

class MyCard(BaseCard):
    def __init__(self, card_id):
        super().__init__(card_id)
        self.add_component('main', MyComponent('main'))

class MyPage(BasePage):
    def __init__(self, page_id):
        super().__init__(page_id, title='Minha Página')
        self.add_card('main', MyCard('main'))

app_daze = WaveApp()
app_daze.add_page('main', MyPage('main'))
app_daze.register_wave_event('meu_evento')

@app("/")
async def serve(q: Q):
    args = app_daze.get_args(q)
    if args:
        q.client.last_event = args.copy() if hasattr(args, 'copy') else dict(args)
    await app_daze.handle_events(q, args=args)
    app_daze.render(q)
    await q.page.save()
```

#### Como acessar valores de campos do formulário no handler
No método `on_<evento>`, basta acessar o valor pelo dicionário `args`:
```python
def on_meu_evento(self, q, state=None, args=None):
    valor = args.get('dummy')
    return f'Você digitou: {valor}'
```

## Comunicação e Propagação de Eventos
- O evento é extraído e normalizado no início do ciclo.
- Se não houver evento, busca-se o último salvo em `q.client.last_event`.
- O evento é propagado do app para a página, card e componente, até ser tratado.
- Cada handler pode retornar True para interromper a propagação.

## Boas Práticas
- Nunca manipule q.args diretamente nos handlers: use sempre o args recebido.
- Use handlers plugáveis para lógica específica de eventos.
- Use o fallback de evento para garantir robustez em navegação e refresh.

## Integração com o Wave
- O DAZE abstrai as diferenças entre @on e @app: use ambos conforme a necessidade.
- O ciclo de eventos é sempre padronizado, independente do ponto de entrada.

## Contribuindo
- Siga o padrão modular e plugável.
- Mantenha a robustez na extração de argumentos e fallback de estado.

---
