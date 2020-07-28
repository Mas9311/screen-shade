import platform


def intro_photo_warning():
    bold = '\x1b[1m'
    undrl = '\x1b[4m'
    lred = '\033[1;31m'
    lgrn = '\033[1;32m'
    cyan = '\033[1;36m'
    clear = '\x1b[0m'

    input_str = (f'\n{bold}{undrl}PHOTOSENSITIVE WARNING{clear}:\n'
                 f'  {cyan}Windows OS{clear} has not been thoroughly tested or optimized.\n'
                 f'  The screen will be redrawn in a crude manner.\n\n'
                 f'** {undrl}May cause epileptic seizures{clear} **\n\n'
                 f'Are you sure you wish to continue?\n'
                 f' - Enter {bold}{lgrn}y{clear} to continue, or anything else to {bold}{lred}quit{clear}.\n'
                 f' > ')

    if input(input_str).lower() != 'y':
        print(f'\nCheck the url below for an update (when it is safe for Windows):\n'
              f' > {lgrn}https://github.com/Mas9311/screen-shade/blob/master/README.md{clear}')
        import sys
        sys.exit()


def init_command(input_str=''):
    windows_os = is_windows_os()
    output = ('python3', 'python.exe')[windows_os] + ' run.py'
    if input_str:
        input_str.strip()
        num_spaces = (3, 0)[windows_os]
        spaces = ' ' * num_spaces
        output += ' ' + input_str + spaces
    return output


def is_windows_os():
    return platform.system() == 'Windows'
