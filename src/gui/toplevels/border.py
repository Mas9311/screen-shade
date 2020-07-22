import sys
from tkinter import Toplevel


class BorderMonitor:
    """Creates each Monitor's Border using the `tkinter.toplevel` widget.
    By default, there are 8 border widgets that encircles the outside of the Monitor.
    Left-clicking on the border widgets bring up the MenuConfig.
    Right-clicking on the border widgets quits the program.
    The width of the border can be modified in the MenuConfig."""
    def __init__(self, creator, monitor):
        self.manager = creator
        self.monitor = monitor

        self.__configure()
        self.__create_widgets()

    def __configure(self):
        self.app = self.manager.app
        self.root = self.app.root

        self.area_list = ['N ', ' E', 'S ', ' W', 'NW', 'NE', 'SW', 'SE']
        self.widgets = dict()

        self.name = self.monitor['name']
        self.w = int(self.monitor['w'])
        self.h = int(self.monitor['h'])
        self.min_x = self.monitor['min_x']
        self.max_x = self.monitor['max_x']
        self.min_y = self.monitor['min_y']
        self.max_y = self.monitor['max_y']

    def __create_widgets(self):
        # if self.name in self.app.config('excluded', w=self.app.get_class('ScreenManager')):
        #     return
        remove_area = list()
        for cardinal in self.area_list:
            curr_tuple = (self.name, cardinal.strip())
            if curr_tuple in self.app.config('border', w=self.app.get_class('ExcludedManager')):
                # do not create this border
                remove_area.append(cardinal)
                continue
            widget = Toplevel()
            widget.overrideredirect(True)
            widget.configure(bg=self.app.config('color', w=self.manager.__class__))
            widget.wait_visibility(widget)
            widget.wm_attributes('-alpha', self.app.config('alpha', w=self.manager.__class__))
            widget.bind('<Button-1>', lambda event, curr_area=cardinal: self.left_click(curr_area))
            widget.bind('<Button-3>', sys.exit)
            self.widgets[cardinal] = widget
        for area in remove_area:
            self.area_list.remove(area)
        self.update_geometries()

    def left_click(self, cardinal):
        if self.app.arg('verbose') > 2:
            print(f'\n{" " * 2}> The {cardinal.strip()} border on monitor {self.name} was clicked.')
        self.app.menuconfig_open()

    def update_geometries(self):
        if self.name in self.app.config('border', w=self.app.get_class('ExcludedManager')):
            print(f'`{self.name}` Monitor\'s border: hidden')
            for cardinal in self.area_list:
                self.widgets[cardinal].geometry(f'1x1+{self.max_x - 1}+{self.max_y - 1}')
            return

        px_radius = self.app.config("px_radius", w=self.manager.__class__)
        two_radius = 2 * px_radius
        for cardinal in self.area_list:
            if cardinal[0] == 'N':
                new_h = px_radius
                new_y = self.min_y
            elif cardinal[0] == 'S':
                new_h = px_radius
                new_y = self.max_y - px_radius
            else:  # !N & !S => vertically-centered plane, i.e. {' E', ' W'}
                new_h = self.h - two_radius
                new_y = self.min_y + px_radius

            if cardinal[1] == 'W':
                new_w = px_radius
                new_x = self.min_x
            elif cardinal[1] == 'E':
                new_w = px_radius
                new_x = self.max_x - px_radius
            else:  # !W & !E => horizontally-centered plane, i.e. {'N ', 'S '}
                new_w = self.w - two_radius
                new_x = self.min_x + px_radius

            geometry_str = f'{new_w}x{new_h}+{new_x}+{new_y}'
            self.widgets[cardinal].geometry(geometry_str)

    # def geometry_left(self):
    #     area = 'Left'
    #     if area not in self.widgets.keys():
    #         return
    #     self.widgets[area].geometry(
    #         f'{self.app.config("px_radius", w=self.manager.__class__)}x'
    #         f'{self.h}+'
    #         f'{self.min_x}+'
    #         f'{self.min_y}')
    #
    # def geometry_right(self):
    #     area = 'Right'
    #     if area not in self.widgets.keys():
    #         return
    #     self.widgets[area].geometry(
    #         f'{self.app.config("px_radius", w=self.manager.__class__)}x'
    #         f'{self.h}+'
    #         f'{self.max_x - self.app.config("px_radius", w=self.manager.__class__)}+'
    #         f'{self.min_y}')
    #
    # def geometry_top(self):
    #     area = 'Top'
    #     if area not in self.widgets.keys():
    #         return
    #     self.widgets[area].geometry(
    #         f'{self.w - (2 * self.app.config("px_radius", w=self.manager.__class__))}x'
    #         f'{self.app.config("px_radius", w=self.manager.__class__)}+'
    #         f'{self.min_x + self.app.config("px_radius", w=self.manager.__class__)}+'
    #         f'{self.min_y}')
    #
    # def geometry_bottom(self):
    #     area = 'Bottom'
    #     if area not in self.widgets.keys():
    #         return
    #     self.widgets[area].geometry(
    #         f'{self.w - (2 * self.app.config("px_radius", w=self.manager.__class__))}x'
    #         f'{self.app.config("px_radius", w=self.manager.__class__)}+'
    #         f'{self.min_x + self.app.config("px_radius", w=self.manager.__class__)}+'
    #         f'{self.max_y - self.app.config("px_radius", w=self.manager.__class__)}')
