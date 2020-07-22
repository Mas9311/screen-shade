from tkinter import *


class GenericToplevel(Toplevel):
    def __init__(self, caller):
        super().__init__()
        self.caller = caller

        self.__configure()
        self.__create()

    def __configure(self):
        self.app = self.caller.app
        self.manager = self.caller.manager

    def __create(self):
        self.overrideredirect(True)
        self.configure(bg=self.app.config('color', w=self.manager.__class__))
        self.wait_visibility(self)
        self.wm_attributes('-alpha', self.app.config('alpha', w=self.manager.__class__))
