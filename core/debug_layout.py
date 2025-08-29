# Adiciona zona de debug ao layout minimal para Wave
from h2o_wave import ui

def add_debug_zone(zones):
    # Adiciona uma zona de debug fixa no rodapé
    zones.append(ui.zone('debug', size='200px'))
    return zones
