from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import platform
import time
from src.defaults import DEFAULT_ARGUMENTS


def retrieve_parameters():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen and halt execution."""
    default = DEFAULT_ARGUMENTS

    usage_str = py_cmd('[options]') + ' ' * 39 + '┃\n\n'
    cmd_description = (
        '         ╔═════════════════════════════════════════════════════╗         ┃\n'
        '         ║ Monitor overlay to lighten or darken monitor output ║         ┃\n'
        '         ╚═════════════════════════════════════════════════════╝         ┃\n'
        '                                                                         ┃\n'
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
    version_description = (
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           \n'
        '        ☐              ☐  screen-shade  v0.0.0  ☐              ☐           \n'
        '        ☐              ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐              ☐           \n'
        '        ☐                                                      ☐           \n'
        '        ☐   Check if there are any new releases for this at:   ☐           \n'
        '        ☐   https://github.com/Mas9311/screen-shade/releases   ☐           \n'
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           ')

    # noinspection PyTypeChecker
    parser = ArgumentParser(add_help=False,
                            description=cmd_description,
                            formatter_class=RawTextHelpFormatter,
                            usage=usage_str)

    parser.add_argument('-d', '--demo',
                        action='store_true',
                        default=default['demo'],
                        dest='demo',
                        help='DEMO: visualizes how the geometry is rendered.' + ' ' * 13 + '┃\n'
                             '  default = %(default)s' + ' ' * 42 + '┃')

    parser.add_argument('-v',
                        action='count',
                        default=default['verbose'],
                        dest='verbose',
                        help='VERBOSE: logs actions to std.out stream.' + ' ' * 19 + '┃\n'
                             '  default = %(default)s' + ' ' * 46 + '┃\n'
                             '  -v   Basic logger' + ' ' * 40 + '┃\n'
                             '  -vv  Advanced debugger' + ' ' * 35 + '┃\n'
                             '  -vvv Developer debugger' + ' ' * 34 + '┃')

    parser.add_argument('--version',
                        action='version',
                        version=version_description,
                        help='VERSION prints to console, and exits.' + ' ' * 22 + '┃')

    parser.add_argument('-h', '--help',
                        action='help',
                        default=SUPPRESS,
                        help='HELP message (this) is displayed, and exits.' + ' ' * 15 + '┃')

    known_args, unknown_args = parser.parse_known_args()

    if unknown_args:  # user added unknown arguments
        # TODO: make an enum for colors: "from enum import Enum; class Color(Enum): ..."
        blink = '\x1b[6m'  # blinks every second
        red = '\x1b[1;31m'  # light red color
        clear = '\x1b[0m'  # clear all formatting (color and font)
        print(f'{blink}{red}*** Fatal Error ***{clear}\n'
              f' > Unknown arguments detected: {str(unknown_args)}\n'
              f' > invoking --help\n')
        parser.print_help()  # prints help message
        time.sleep(0.25)  # pause execution just long enough for help to display
        parser.parse_args()  # prints error message and halts the execution

    # converts the execution's arguments from a Namespace type => dictionary type
    arg_dict = {
        'verbose': known_args.verbose,
        'demo': known_args.demo,
        # 'file': known_args.file,  # TODO: implement -f, --file
    }

    return arg_dict


def py_cmd(additional=''):
    windows_os = platform.system() == 'Windows'
    cmd = ('python3', 'python.exe')[windows_os] + ' run.py'
    if additional:
        additional.strip()
        num_spaces = (3, 0)[windows_os]
        spaces = ' ' * num_spaces
        cmd += ' ' + additional + spaces
    return cmd
