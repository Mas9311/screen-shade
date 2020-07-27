#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src import *
from sys import platform


if __name__ == '__main__':
    # TODO: implement parse_args.py
    arg_dict = {
        'verbose': 0,
        'demo': False
    }

    if platform in ['win32', 'cygwin']:
        # OS is Windows
        input_str = (f'\nPHOTOSENSITIVE WARNING:\n'
                     f'  Windows OS has not been thoroughly tested or optimized.\n'
                     f'  The screen will be redrawn in a crude manner.\n\n'
                     f'**May cause epileptic seizures.**\n\n'
                     f'Are you sure you wish to continue?\n'
                     f' - Enter `y` to continue. Enter anything else to quit.\n'
                     f' > ')
        if input(input_str).lower() != 'y':
            sys.exit()
    else:
        # running 2 instances of this program? Terminate first process with SIGTERM.
        kill_all_running_instances(__file__, arg_dict['verbose'])

    correct_cwd()  # cd /.../shade*/

    root = Tk()
    App(root, arg_dict)
    root.mainloop()
