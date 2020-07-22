from tkinter import GROOVE, FLAT

from src.gui.toplevels.generic_toplevel import GenericToplevel


class ScreenArea:
    def __init__(self, creator, monitor_index, mouse_focused=False):
        self.manager = creator
        self.index = monitor_index
        self.focus = mouse_focused
        self.hidden = None

        self.widgets = dict()

        self.__configure()
        self.__create_widgets()

        # self.hidden_screen_check()

    def __configure(self):
        self.app = self.manager.app
        self.root = self.app.root
        self.monitor = self.app.monitors[self.index]

        self.name = self.monitor['name']
        self.w = self.monitor['w']
        self.h = self.monitor['h']
        self.min_x = self.monitor['min_x']
        self.max_x = self.monitor['max_x']
        self.min_y = self.monitor['min_y']
        self.max_y = self.monitor['max_y']

        # self.hidden = self.monitor['hidden']
        self.hidden_geometry_str = '0x0+0+0'

    def __create_widgets(self):
        """"""
        for cardinal in self.app.cardinal_list + ['full']:
            self.create_toplevel_widget(cardinal)

        self.update_widget_geometry(init=True)
        self.update_demo()

    def create_toplevel_widget(self, cardinal):
        widget = GenericToplevel(self)
        if cardinal == 'full':
            widget.bind('<Motion>', lambda event, index=self.index: self.manager.reconstruct_monitor_focused(index))
        else:
            widget.bind('<Motion>', lambda event: self.app.mouse_motion())

        # widget.bind('<Enter>', self.app.mouse_motion)
        # widget.bind('<Button>', self.app.mouse_motion)
        # widget.bind('<Leave>', self.app.mouse_motion)

        # widget.bind('<B1-Motion>', self.app.mouse_motion)
        # widget.bind('<Button-1>', sys.exit)
        # widget.bind('<Escape>', self.key_press)
        self.widgets[cardinal] = widget

    def focus_change(self):
        self.focus = not self.focus
        self.update_widget_geometry()

    def geometry_1(self):
        """Cover the entire monitor in one generic transparent widget"""
        border_buffer = self.app.config('px_radius', w=self.app.get_class('BorderManager'))
        self.widgets['full'].geometry(
            f'{self.w - 2 * border_buffer}x'
            f'{self.h - 2 * border_buffer}+'
            f'{self.min_x + border_buffer}+'
            f'{self.min_y + border_buffer}'
        )

    def geometry_8(self, mouse_center=False, mouse_refresh=True):
        """Reconfigure all 8 cardinal direction widgets on the configured monitor `focused`
        1111233      NW N~ NE
        1111233      ~W ~~ ~E
        4444 55      SW S~ SE
        6666788
        """
        if mouse_center:
            mouse_x, mouse_y = self.app.center_mouse_opening()
        else:
            mouse_x, mouse_y = self.app.get_mouse_coords(mouse_refresh)  # update and store the mouse_{x, y} coordinates.
        px_radius = self.app.config('px_radius', w=self.manager.__class__)
        border_buffer = self.app.config('px_radius', w=self.app.get_class('BorderManager'))
        two_radius = 2 * px_radius

        rel_mouse_x = mouse_x - self.min_x
        width_west = rel_mouse_x - px_radius
        width_east = self.w - rel_mouse_x - px_radius
        mouse_west = mouse_x - px_radius
        mouse_east = mouse_x + px_radius

        rel_mouse_y = mouse_y - self.min_y
        height_north = rel_mouse_y - px_radius
        height_south = self.h - rel_mouse_y - px_radius
        mouse_north = mouse_y - px_radius
        mouse_south = mouse_y + px_radius

        for cardinal in self.app.cardinal_list:
            # Top, Bottom, middle
            if cardinal[0] == 'N':
                new_h = height_north - border_buffer
                new_y = self.min_y + border_buffer
            elif cardinal[0] == 'S':
                new_h = height_south - border_buffer
                new_y = mouse_south
            else:  # !N & !S => vertically-centered plane: {' E', ' W'}
                new_h = two_radius
                new_y = mouse_north

            # Left, Right, middle
            if cardinal[1] == 'W':
                new_w = width_west - border_buffer
                new_x = self.min_x + border_buffer
            elif cardinal[1] == 'E':
                new_w = width_east - border_buffer
                new_x = mouse_east
            else:  # !W & !E => horizontally-centered plane: {'N ', 'S '}
                new_w = two_radius
                new_x = mouse_west

            geometry_str = f'{new_w}x{new_h}+{new_x}+{new_y}'
            if new_w <= 0 or new_h <= 0:
                geometry_str = self.hidden_geometry_str  # 0x0 pixels
                if self.app.arg('verbose') > 1:
                    print(f'{" " * 4}- ScreenArea widget \'{cardinal}\' contains a geometry value <= 0.\n'
                          f'{" " * 6}> setting \'{cardinal}\' geometry to \'{geometry_str}\'.')

            if self.app.arg('verbose') > 2:
                print(f'\'{cardinal}\': {geometry_str}')
            self.widgets[cardinal].geometry(geometry_str)
        if self.app.arg('verbose') > 2:
            print()

    def hidden_screen_check(self):
        if self.name in self.app.config('screen', w=self.app.get_class('ExcludedManager')):
            self.widgets_hide()
            return True
        return False

    def update_widgets_hidden(self):
        print("Updating hidden widgets")
        if self.hidden:
            print("Seen => Unseen")
            self.widgets_hide()
        else:
            print("Unseen => Seen")
            self.widgets_reveal()

    def widgets_hide(self):
        # if not self.hidden:
        #     self.app.widget('ExcludedManager').hidden_update_variables_screen(monitor=self.monitor)

        for curr_widget in self.widgets.values():
            curr_widget.geometry(self.hidden_geometry_str)  # 0x0 pixels in top-left corner

    def widgets_reveal(self):
        # if self.hidden:
        #     self.app.widget('ExcludedManager').hidden_update_variables_screen(monitor=self.monitor)
        self.update_widget_geometry()

    def update_demo(self):
        if not self.app.arg('demo'):  # Hide demo
            new_relief = FLAT
            new_border = 0
        else:  # Display demo
            new_relief = GROOVE
            new_border = 5

        for curr_area in self.widgets.values():
            curr_area.configure(relief=new_relief, borderwidth=new_border)

    def update_widget_geometry(self, mouse_center=False, mouse_refresh=True, init=False):
        if not init and self.hidden_screen_check():
            print("Not updating ScreenArea, because hidden")
            return
        elif self.focus:
            # full => 8
            self.widgets['full'].geometry(self.hidden_geometry_str)
            self.geometry_8(mouse_center=mouse_center, mouse_refresh=mouse_refresh)
        else:
            # 8 => full
            for cardinal in self.app.cardinal_list:
                self.widgets[cardinal].geometry(self.hidden_geometry_str)
            self.geometry_1()
