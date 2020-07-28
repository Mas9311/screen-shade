from src.gui.managers.border import BorderManager
from src.gui.toplevels.menu import MenuConfig
from src.gui.managers.excluded import ExcludedManager
from src.gui.managers.screen import ScreenManager


PX_RADIUS = 20
# TODO: center MenuConfig[{x,y}] on Shade._monitors[0].
# TODO: remove my custom [MonitorManager]['excluded'] list
DEFAULT_CONFIGURATIONS = {
    BorderManager: {
        'alpha': 0.75,
        'color': '#4B8BBE',
        'px_radius': PX_RADIUS // 2,
    },
    MenuConfig: {
        'alpha': 0.50,
        'color': {
            'border': '#6900db',
            'inner': '#303030',
        },
        'w': 200,
        'h': 300,
        'x': 0,
        'y': 0,
    },
    ExcludedManager: {
        'border': [('HDMI-0', 'N')],
        'screen': {'HDMI-0'},
    },
    ScreenManager: {
        'alpha': 0.40,
        'color': '#000000',
        'px_radius': PX_RADIUS,
    },
}

DEFAULT_ARGUMENTS = {
    'verbose': 0,
    'demo': False,
}
