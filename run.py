#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src import *

if __name__ == '__main__':
    arg_dict = retrieve_parameters()

    if is_windows_os():
        # OS is Windows
        intro_photo_warning()
    else:
        # running 2 instances of this program? Terminate first process with SIGTERM.
        kill_all_running_instances(__file__, arg_dict['verbose'])

    correct_cwd()  # cd /.../shade*/

    root = Tk()
    App(root, arg_dict)
    root.mainloop()
