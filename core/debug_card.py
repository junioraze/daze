# DebugCard for DAZE: UI card to display debug logs if debug mode is enabled
from h2o_wave import ui, Q
from core.debug import DebugManager

class DebugCard:
    @staticmethod
    def render(q: Q, visible: bool = True):
        debug = DebugManager.get_instance()
        if not debug.enabled or not visible:
            q.page['debug'] = None
            return
        logs = debug.get_logs()
        q.page['debug'] = ui.markdown_card(
            box='debug',
            title='Debug Log',
            content='\n'.join(f'- {line}' for line in logs[-20:]) or '_No logs yet._'
        )
