#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyautogui
# import screeninfo
import sys
import time

from src import *
from src.gui import *
from src.helpers import *


class App:
    def __init__(self, parent):
        self.root = parent
        self.root.geometry('0x0+0+0')
        self.root.configure(bg='#000000')

        pyautogui.FAILSAFE = False

        self.alpha = 80  # range of [0, qq100]. converted to [0, 1]
        self.alpha_busy = False
        self.alpha_offset = -.01  # alpha cannot stay EXACTLY the same when setting root.wm_attribute(-alpha)
        self.first_time_configuring = True

        self.__bind()
        self.__transparent()
        self.__configure()
        self.__fullscreen()
        self.brighten()
        self.root.update_idletasks()

    def __bind(self):
        self.root.bind('<Button-1>', self.click)
        self.root.bind('<Button-3>', sys.exit)
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Left>', self.adjust_alpha)
        self.root.bind('<Right>', self.adjust_alpha)
        self.root.bind('<Up>', self.adjust_alpha)
        self.root.bind('<Down>', self.adjust_alpha)
        self.root.bind('<Escape>', self.key_press)

        # self.root.bind('<Double-Button-1>', sys.exit)
        # self.root.bind('<ButtonRelease-1>', self.click_release)

    def __transparent(self):
        if self.first_time_configuring:
            start_x, start_y = pyautogui.position()
            pyautogui.moveTo(1, 1)  # moves mouse to the upper-leftmost monitor.
            self.root.wait_visibility(self.root)
            pyautogui.moveTo(start_x, start_y)  # reverts mouse position back to start

        self.adjust_alpha()

    def __configure(self):
        if self.first_time_configuring:
            self.first_time_configuring = False
            total_w, total_h = pyautogui.size()
            self.root.geometry(f'{total_w}x{total_h}+0+0')
            print(f'{"·" * 19}\n:  Width x Height :\n:{f" {total_w}px": >7} x {f"{total_h}px ": <6}:\n{"·" * 19}')
            print('Geometry:', self.root.geometry())
            self.root.resizable(width=False, height=False)
            self.root.wm_attributes("-topmost", 1)

        self.root.overrideredirect(True)

    def __fullscreen(self):
        # self.root.attributes('-zoomed', True)
        self.root.wm_attributes('-fullscreen', True)

    def adjust_alpha(self, event=None):
        """While the widget has the focus, pressing Left|Right key will adjust transparency.
        [Light] 000---------------x---100 [Dark]
        Left key makes the widget lighter.
        Right key makes the widget darker."""
        diff = 0
        if event is None:
            pass
        elif event.keysym in ['Right', 'Up']:
            diff = 5
        elif event.keysym in ['Left', 'Down']:
            diff = -5

        if 0 <= self.alpha + diff <= 100:
            self.alpha += diff
        alpha_normalized = self.get_new_alpha() / 100
        print(f'Transparency: {self.alpha}%')

        # LINUX
        self.root.wm_attributes('-alpha', alpha_normalized)
        # # ? WINDOWS/UNIX ?
        # self.root.attributes(alpha=alpha_normalized)

    def click(self, event):
        if self.alpha_busy:
            print(f'{"·" * 27}\n:Busy handling first click:\n{"·" * 27}')
            return

        self.alpha_busy = True
        clicked_x, clicked_y = pyautogui.position()
        time.sleep(0.15)
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.dim()
        self.root.iconify()
        pyautogui.click(x=clicked_x, y=clicked_y)
        time.sleep(0.15)
        print(f'click at: x={clicked_x}, y={clicked_y}')
        self.root.deiconify()
        self.brighten()
        self.__transparent()
        self.__configure()
        self.alpha_busy = False

    def dim(self):
        print(f'\n  Dimming from {self.alpha}% => 0%')
        temp = self.alpha
        while temp > 0:
            self.root.wm_attributes('-alpha', temp / 100)
            self.root.update()
            time.sleep(0.0009)
            temp -= 1

    def brighten(self):
        print(f'  Brightening from 0% => {self.alpha}%')
        temp = 0
        while temp < self.alpha:
            self.root.wm_attributes('-alpha', temp / 100)
            self.root.update()
            time.sleep(0.005)
            temp += 1

    def get_new_alpha(self):
        self.alpha_offset *= -1
        return self.alpha + self.alpha_offset

    def key_press(self, event):
        if event.keysym == 'Escape' or event.char.lower() == 'q':
            sys.exit()
        elif event.char.lower() == '1':
            self.root.configure(bg='#000000')
        elif event.char.lower() == '0':
            self.root.configure(bg='#ffffff')
        elif event.char.lower() == '2':
            self.root.configure(bg='#0000ff')
        elif event.char.lower() == '3':
            self.root.configure(bg='#00ff00')
        elif event.char.lower() == '4':
            self.root.configure(bg='#ff0000')
        elif event.char.lower() == '5':
            self.root.configure(bg='#4A009B')

    # def click_release(self, event):
    #     pass


# if __name__ == '__main__':
#     pyautogui.FAILSAFE = False
#     root = Tk()
#     app = App(root)
#     root.mainloop()
