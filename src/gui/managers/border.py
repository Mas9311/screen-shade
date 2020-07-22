from src.gui.toplevels.border import BorderMonitor


class BorderManager:
    def __init__(self, creator):
        self.app = creator

        self.__configure()
        self.__create_widgets()

    def __configure(self):
        self.root = self.app.root

    def __create_widgets(self):
        self.widgets = [BorderMonitor(self, curr_monitor) for curr_monitor in self.app.monitors]

    def adjust_px_radius(self, value):
        value = int(value)
        print(f'Adjusting {self.__class__.__name__} px_radius to {value}')
        self.app.config('px_radius', w=self.__class__, set=value)

        for curr_monitor in self.widgets:
            curr_monitor.update_geometries()
        self.app.widget('ScreenManager').update_border_geometry(mouse_center=True)
