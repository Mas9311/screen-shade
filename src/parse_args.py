from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import platform
import time
from src.defaults import DEFAULT_ARGUMENTS


def retrieve_parameters():
    """Retrieves the parameters from the console if provided.
    Returns the parameters in dict format.
    If an unknown argument is passed, print the --help screen.
    If no arguments are passed, then print the intro Welcome screen."""

    version_description = (
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           \n'
        '        ☐              ☐  screen-shade  v0.0.0  ☐              ☐           \n'
        '        ☐              ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐              ☐           \n'
        '        ☐                                                      ☐           \n'
        '        ☐   Check if there are any new releases for this at:   ☐           \n'
        '        ☐   https://github.com/Mas9311/screen-shade/releases   ☐           \n'
        '        ☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐           '
    )

    default = DEFAULT_ARGUMENTS

    cmd_description = (
        '⠀⠀⠀⠀⠀⠀⠀╔═════════════════════════════════════════════════════╗⠀⠀⠀⠀⠀⠀⠀┃\n'
        '⠀⠀⠀⠀⠀⠀⠀║ Monitor overlay to lighten or darken monitor output ║⠀⠀⠀⠀⠀⠀⠀┃\n'
        '⠀⠀⠀⠀⠀⠀⠀╚═════════════════════════════════════════════════════╝⠀⠀⠀⠀⠀⠀⠀┃\n'
        '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀┃\n'
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
    )

    # noinspection PyTypeChecker
    parser = ArgumentParser(add_help=False,
                            description=cmd_description,
                            formatter_class=RawTextHelpFormatter,
                            usage=py_cmd('[options]') + (' ' * 39) + '┃')

    parser.add_argument('-d', '--demo',
                        action='store_true',
                        default=default['demo'],
                        dest='demo',
                        help='Demo:    default = %(default)s' + ' ' * 38)

    parser.add_argument('-v',
                        action='count',
                        default=default['verbose'],
                        dest='verbose',
                        help='Verbose: default = %(default)s.' + ' ' * 41 + '\n'
                             ' -v   Basic logger\n'
                             ' -vv  Advanced debugger\n'
                             ' -vvv Developer debugger')

    parser.add_argument('--version',
                        action='version',
                        version=version_description,
                        help='VERSION prints to console, and exits')

    parser.add_argument('-h', '--help',
                        action='help',
                        default=SUPPRESS,
                        help='HELP message (this) is displayed, and exits')

    known_args, unknown_args = parser.parse_known_args()

    if unknown_args:  # user added unknown arguments
        print(f'Unknown arguments detected: {str(unknown_args)}\n > calling --help screen\n')
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
    cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'
    if additional:
        additional.strip()
        num_spaces = 0 if platform.system() == 'Windows' else 3
        spaces = ' ' * num_spaces
        cmd += ' ' + additional + spaces
    return cmd
