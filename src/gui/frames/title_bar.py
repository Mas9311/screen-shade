from tkinter import *

from src.gui.frames.window_manager import WindowManager


class Titlebar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, background='#505050', padx=0, pady=0)
        self.caller = master

        self.__configure()
        self.__create_widgets()

    def __configure(self):
        self.app = self.caller.app
        self.root = self.app.root
        self.__initialize_offsets()

        self.widgets = dict()

    def __create_widgets(self):
        # bind translate the widget's (x, y) coordinate
        self.bind('<Button-1>', self._init_translate)  # start of movement
        self.bind('<B1-Motion>', self._motion_translate)  # currently moving, update (x, y) coordinates
        self.bind('<ButtonRelease-1>', self._term_translate)  # finish moving
        self.columnconfigure(index=0, weight=1)

        self.widgets[WindowManager] = WindowManager(self)
        self.widgets[WindowManager].grid(row=0, column=1)  # place(relx=0, rely=0, anchor=NW)

    def __initialize_offsets(self):
        self.offset_dim = {
            'x': 0,
            'y': 0
        }

    def _init_translate(self, event):
        self.valid_translation = isinstance(event.widget, self.__class__)
        if self.app.arg('verbose'):
            print(f'{" " * 1}> Clicked Titlebar: valid_translation={self.valid_translation}')
        if self.valid_translation:
            self.offset_dim['x'] = event.x
            self.offset_dim['y'] = event.y
        if self.app.arg('verbose') > 1:
            print(f'{" " * 3}- offset_dim={self.offset_dim}')

    def _motion_translate(self, _):
        if self.valid_translation:
            new_x = self.caller.winfo_pointerx() - self.offset_dim['x']
            new_y = self.caller.winfo_pointery() - self.offset_dim['y']
            self.app.config('x', w=self.caller.__class__, set=new_x)
            self.app.config('y', w=self.caller.__class__, set=new_y)
            self.caller.geometry(f'+{new_x}+{new_y}')

    def _term_translate(self, _):
        self.valid_translation = False
        self.__initialize_offsets()
        self.app.update_monitor_focused()
