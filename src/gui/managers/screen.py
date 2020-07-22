from src.gui.toplevels.screen import ScreenArea


class ScreenManager:
    def __init__(self, creator):
        self.app = creator

        self.configured_index = None  # monitor index of current mouse location i.e. `focused`
        self.hidden_monitors = set()

        self.__configure()
        self.__create_widgets()

    def __configure(self) -> None:
        self.root = self.app.root
        self.configured_index = self.app.get_monitor_index()

    def __create_widgets(self) -> None:
        self.widgets = list()

        for index, monitor in enumerate(self.app.monitors):
            # either ``the mouse isn't on this Monitor`` or ``the mouse is somewhere on this Monitor``
            contains_mouse = (False, True)[self.configured_index == index]
            self.widgets.append(ScreenArea(self, index, contains_mouse))

    def adjust_alpha(self, value) -> None:
        value = float(value)
        print(f'Adjusting ScreenArea transparency to {int(value * 1000) / 10}%')
        self.app.config('alpha', w=self.__class__, set=value)
        for screenarea in self.widgets:
            for area_widget in screenarea.widgets.values():
                area_widget.wm_attributes('-alpha', self.app.config('alpha', w=self.__class__))

    def adjust_color(self, value) -> None:
        print(f'Adjusting ScreenArea color to {value}.')
        self.app.config('color', w=self.__class__, set=value)
        for screenarea in self.widgets:
            for area_widget in screenarea.widgets.values():
                area_widget.configure(bg=self.app.config('color', w=self.__class__))

    def adjust_px_radius(self, value) -> None:
        value = int(value)
        print(f'Adjusting ScreenArea mouse radius to {value}')
        self.app.config('px_radius', w=self.__class__, set=value)
        self.app.center_mouse_opening()
        self.update_screen_areas()

    def check_for_hidden_screens(self):
        for curr in self.widgets:
            curr.hidden_screen_check()

    def update_demo(self) -> None:
        print(f'Recreating ScreenArea demo to {self.app.arg("demo")}')
        for monitor_w in self.widgets:
            monitor_w.update_demo()

    def reconstruct_monitor_focused(self, new_index) -> None:
        print('> Mouse switched monitors.')
        old_configured_index = self.configured_index
        self.configured_index = new_index
        if self.app.arg('verbose') > 1:
            print(f'\n{"*" * 35}\nSTART: Reconstructing ScreenAreas\n{"*" * 35}\n'
                  f'{" " * 4}{old_configured_index}: \'{self.app.monitors[old_configured_index]["name"]}\' => '
                  f'{self.configured_index}: \'{self.app.monitors[self.configured_index]["name"]}\'')

        self.widgets[old_configured_index].focus_change()
        self.widgets[self.configured_index].focus_change()

        # self.app.recreate_config_menu()

        if self.app.arg('verbose') > 1:
            print(f'{"*" * 35}\nFINISH: Reconstructing ScreenAreas\n{"*" * 35}\n')

    def update_hidden(self, index):
        # self.widgets[monitor['index']].hidden_update_variables(hide_widgets=not monitor['hidden'])
        self.widgets[index].update_widgets_hidden()

    def update_screen_areas(self, mouse_center=False, mouse_refresh=False) -> None:
        self.widgets[self.configured_index].update_widget_geometry(mouse_center=mouse_center,
                                                                   mouse_refresh=mouse_refresh)

    def update_border_geometry(self, mouse_center=False, mouse_refresh=False) -> None:
        for monitor in self.widgets:
            monitor.update_widget_geometry(mouse_center=mouse_center, mouse_refresh=mouse_refresh)
