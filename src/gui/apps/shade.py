#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyautogui
import screeninfo
import sys
# import time

from src.gui.managers.border import BorderManager
from src.gui.managers.demo import DemoManager
from src.gui.managers.excluded import ExcludedManager
from src.gui.toplevels.menu import MenuConfig
from src.gui.managers.screen import ScreenManager
from src.helpers.file_helper import import_configurations, export_to_file


class App:
    """Creates transparent rectangles covering the span of all monitors.
    The monitor containing the current mouse location contains 8 boxes; 1 for each of the `8-wind` cardinal directions:
      - NW, N~, NE
      - ~W,     ~E
      - SW, S~, SE
    The 4 corners contain the majority of the screens, therefore are created first.
    The 4 cardinal directions {N, S, E, W} are thin strips, and are created last.

    This leaves one square for the mouse to maintain focus on the underlying applications.
     - e.g.: a mouse radius of 10 pixels, Dia=20. Total area = 20x20 = 400 pixels 'window'
    Any other monitor (if more than 1) that does not currently hold the mouse's focus
      is covered in a `full` rectangle, spanning the entire monitor.

    A 1-pixel radius is allowed on every border of every monitor to not hinder with your OS's toolbar
      (namely when intelligently hidden), i.e. hover over the border to bring up the toolbar.

    Clicking on the border of any monitor brings up a menu to customize this application's settings.
    """
    def __init__(self, master, arg_dict):
        self.root = master
        self._arg_dict = arg_dict

        # self.app, self.manager = self, self
        self.class_helper = ClassHelper(self, __name__)
        self._config_dict = import_configurations(self)

        self._mouse_x, self._mouse_y = None, None  # current positions
        self._mouse_in_motion = False

        self.cardinal_list = ['NW', 'NE', 'SW', 'SE', 'N ', ' W', 'S ', ' E']
        # self.screeninfo_monitors = screeninfo.get_monitors()
        self.monitors = []
        self._widgets = {}

        self.__configure_root()
        self.__create_widgets()
        self.root.tkraise()

    def __configure_root(self):
        # make root a 0x0 box in the top-left corner (obsolete widget)
        self.root.geometry('0x0+0+0')
        self.root.overrideredirect(True)
        self.root.bind('<Button-3>', sys.exit)  # Right click will quit the execution

        # In case we wanted the application to show in the OS's currently-running-applications bar.
        # from tkinter import PhotoImage
        # self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='./graphics/shades.png'))
        # self.root.title('Shadow')
        # self.root.configure(bg='#4A009B')
        # self.root.iconify()

    def __create_widgets(self):
        self.__init_monitor_meta()
        self._mouse_in_motion = True
        self.refresh_mouse_xy(False)
        self._widgets[DemoManager] = DemoManager(self)
        self._widgets[ScreenManager] = ScreenManager(self)
        self._widgets[BorderManager] = BorderManager(self)
        self._widgets[ExcludedManager] = ExcludedManager(self)

        self.check_for_hidden_widgets()

        self._mouse_in_motion = False

    def __init_monitor_meta(self):
        for index, monitor in enumerate(screeninfo.get_monitors()):
            # convert type: screeninfo::Monitor => dict
            self.monitors += [{
                'name': monitor.name,
                'w': int(monitor.width),
                'h': int(monitor.height),
                'min_x': int(monitor.x),
                'max_x': int(monitor.x + monitor.width),
                'min_y': int(monitor.y),
                'max_y': int(monitor.y + monitor.height),
                'hidden': monitor.name in self.config('screen', w=self.get_class('ExcludedManager')),
                'index': index,
            }]

        print(f'Monitor{("", "s")[len(self.monitors) > 1]} found:')
        for index, monitor in enumerate(self.monitors):
            print(f'{(" " * 9, " Primary:")[index == 0]}[{index}] = {monitor}')
        print()

    def arg(self, key, **kwargs):
        """Modifies or Retrieves the executable arguments' dictionary, ``arg_dict``"""
        if 'set' not in kwargs:
            # This method is a used as a getter(), Return the value stored in `execution's arguments` dict
            return self._arg_dict[key]
        # Used as a setter(), Set the executable argument value.
        self._arg_dict[key] = kwargs['set']

    def config(self, *args, **kwargs):
        """Modifies or Retrieves the class variable, ``config_dict``.
        depending on if the kwarg['set'] is included.
        Note: this method MUST be called with the kwarg['w'] (the ``widget class`` requested)."""
        if 'w' not in kwargs:
            print(f'\n\n\n{"@" * 3}- Called app._config_dict without a widget, ``w``. Examples:\n'
                  f'\tself.app.config(\'alpha\', w=ScreenManager)'
                  f'\tself.app.config(\'color\', \'border\', w=MenuConfig, set=\'#00FF00\')\n\n\n')
            sys.exit()
        args = [_ for _ in args]  # transform (tuple) into [list]
        class_ = kwargs['w']
        last_key = args.pop(-1)

        pointer = self._config_dict[class_]
        for arg in args:
            # traverse nested dicts until we have the last dict
            pointer = pointer[arg]

        if 'set' in kwargs:
            # sets the value in the last dict -- the purpose of using the pointer variable.
            if self.arg('verbose') > 1:
                print(f'Setting config_dict {last_key} in {pointer} to {kwargs["set"]}')
            pointer[last_key] = kwargs['set']
            # if 'export' in kwargs and not kwargs['export']:
            #     return
            export_to_file(self._config_dict, self.arg('verbose'))  # write to file.
        else:
            # gets the value stored and return it.
            return pointer[last_key]

    def class_list_str(self) -> list:
        return self.class_helper.class_list_str()

    def class_list(self) -> list:
        return self.class_helper.class_list()

    def get_class(self, class_str):
        return self.class_helper.get_class(class_str)

    def widget(self, class_str: str):
        return self._widgets[self.get_class(class_str)]

    def center_mouse_opening(self):
        curr_monitor_index = self.get_monitor_index()
        if curr_monitor_index == -1:
            print('*** Cannot locate which monitor the mouse is currently on. Defaulting to monitor [0]. ***')
            curr_monitor_index = 0
        while curr_monitor_index in self.widget('ScreenManager').hidden_monitors:
            curr_monitor_index = (curr_monitor_index + 1) % (len(self.monitors) - 1)
            print(curr_monitor_index)

        monitor = self.monitors[curr_monitor_index]
        if self._arg_dict['verbose'] > 1:
            print(f'{" " * 3}> Centering mouse opening on {monitor["name"]}: {monitor}')
        self._mouse_x = monitor['w'] // 2 + monitor['min_x']
        self._mouse_y = monitor['h'] // 2 + monitor['min_y']
        return self.get_mouse_coords(mouse_refresh=False)

    def check_for_config_menu_open(self):
        pass

    def check_for_hidden_widgets(self):
        print('All widgets created. Checking for hidden widgets')
        self._widgets[ScreenManager].check_for_hidden_screens()

    def config_menu_open(self, mouse=True):
        if MenuConfig in self._widgets:
            print('* Configuration Menu is already open.')
            return

        if self.arg('verbose'):
            print(f'- Creating MenuConfig widget')
        self._widgets[MenuConfig] = MenuConfig(self)

        if mouse:
            self.move_mouse_to_config_menu()

        self.update_monitor_focused()

    def configmenu_close(self, destroyed=False, recreate=False):
        """Destroying the MenuConfig widget takes a long time, so
        First:   save it as a local variable,
        Then:    delete the key from the dict (which allows it to be recreated before ``fully`` destroying),
        Finally: fully-destroy the widget in the next-available free time.

        Note: Two Toplevel::MenuConfig widgets may exist simultaneously (on top of each other),
              but only temporarily (for < ~100 ms depending on cpu ``strength``)."""

        if self.arg('verbose') > 2:
            print(f'{" " * 3}> Closing MenuConfig.\n'
                  f'{" " * 5}- widgets[MenuConfig] exists? {MenuConfig in self._widgets}')
        if MenuConfig in self._widgets.keys():
            configmenu = self._widgets[MenuConfig]
            configmenu.configure(background='#000000')
            del self._widgets[MenuConfig]

            configmenu.geometry('100x100+0+0')
            if not destroyed:
                configmenu.destroy_()
                configmenu.destroy()  # destroy the main Toplevel::MenuConfig widget itself (gray colored)

            if recreate:
                self.config_menu_open(mouse=False)

    def get_max_screen_dimensions(self):
        return pyautogui.size()

    def get_mouse_coords(self, mouse_refresh=True, oob=True):
        if mouse_refresh:
            self.refresh_mouse_xy(oob)
        return self._mouse_x, self._mouse_y

    def get_monitor_index(self):
        curr_x, curr_y = pyautogui.position()
        for index, monitor in enumerate(self.monitors):
            if monitor['min_x'] <= curr_x <= monitor['max_x']:
                if monitor['min_y'] <= curr_y <= monitor['max_y']:
                    return index
        return -1

    def move_mouse_to_config_menu(self):
        """Moves mouse to center of MenuConfig's Titlebar widget."""
        title_width, title_height = self._widgets[MenuConfig].get_titlebar_wh()
        new_x = title_width // 2 + self.config('x', w=MenuConfig)
        new_y = title_height // 2 + self.config('y', w=MenuConfig)
        if self.arg('verbose') > 1:
            print(f' > Moving mouse to ({new_x}, {new_y})')

        try:
            pyautogui.moveTo(x=new_x, y=new_y)
        except pyautogui.FailSafeException:
            if self.arg('verbose'):
                print(f'*** Caught pyautogui.FailSafeException: .moveTo() mouse coordinates out of bounds.')
                if self.arg('verbose') > 1:
                    print(f' > Adjusting coordinates: ({new_x}, {new_y}) => {self.get_mouse_coords(True, False)}\n')

    def mouse_motion(self):
        if self._mouse_in_motion:
            return

        self._mouse_in_motion = True
        self.refresh_mouse_xy()  # update self.{mouse_x, mouse_y} vars
        self._widgets[ScreenManager].update_screen_areas()  # update the geometry of the areas covering the screen

        # self.root.update_idletasks()
        # time.sleep(.0017)
        self._mouse_in_motion = False

    def refresh_mouse_xy(self, oob=True):
        self._mouse_x, self._mouse_y = pyautogui.position()
        if not oob:
            return  # do not correct the oob (out-of-bounds) pixel radius

        border_buffer = self.config('px_radius', w=BorderManager)
        curr_monitor = self.monitors[self.get_monitor_index()]
        mouse_radius = self.config('px_radius', w=ScreenManager)
        min_x = curr_monitor['min_x'] + mouse_radius + border_buffer
        max_x = curr_monitor['max_x'] - mouse_radius - border_buffer
        min_y = curr_monitor['min_y'] + mouse_radius + border_buffer
        max_y = curr_monitor['max_y'] - mouse_radius - border_buffer

        self._mouse_x = max(self._mouse_x, min_x)  # [L] set to min-in-bounds pixel
        self._mouse_x = min(self._mouse_x, max_x)  # [R] set to max-in-bounds pixel
        self._mouse_y = max(self._mouse_y, min_y)  # [T] set to min-in-bounds pixel
        self._mouse_y = min(self._mouse_y, max_y)  # [B] set to max-in-bounds pixel

    def update_monitor_focused(self):
        if self._widgets[ScreenManager].configured_index != self.get_monitor_index():
            print('Must switch focused monitors')
            self._widgets[ScreenManager].reconstruct_monitor_focused(self.get_monitor_index())
            # self.center_mouse_opening()
            # pyautogui.moveTo(self._mouse_x, self._mouse_y)
            # self.widgets[ScreenManager].update_screen_areas()


class ClassHelper:
    def __init__(self, master, __name):
        self.app = master
        self.__name = __name

    def class_list_str(self) -> list:
        output = dir(sys.modules[self.__name])[1:7]
        # print(output)
        return output

    def class_list(self) -> list:
        output = [getattr(sys.modules[self.__name], f'{class_str}') for class_str in self.class_list_str()]
        # print(output)
        return output

    def get_class(self, class_str):
        for curr_class in self.class_list():
            # print(f'Does {class_str} == {curr_class.__name__}? {class_str == curr_class.__name__}')
            if curr_class.__name__ == class_str:
                return curr_class
        print(f'Error: class `{class_str}` not found in list of classes.')
        sys.exit()
