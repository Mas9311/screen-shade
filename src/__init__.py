# """An import statement of 'from src import *' will import the following:"""
from tkinter import *
from src.gui.apps import App
from src.helpers.os_helpers import intro_photo_warning, is_windows_os
from src.helpers.path_helper import correct_cwd
from src.helpers.process_helper import kill_all_running_instances
from src.parse_args import retrieve_parameters

# print('Imported src/__init__.py')
