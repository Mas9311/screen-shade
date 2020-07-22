import os
import sys


"""This file helps automate the ``os.path`` methods.

The ``/.../shade/data/`` dir will contain the ``configurations.txt`` file.

There are two (2) constants defined in this file (located at the bottom):
  get_data_path() (str): the absolute path to the ``/.../shade/data/`` directory.
  get_config_path (str): the absolute path to the ``/.../shade/data/configurations.txt`` file.

Note: The correct_cwd function will be executed first. This will change directories,
  so any paths therein will be the shade program's directory, and not the directory
  that the program was executed from, like "/bin/pwd".

"""


def correct_cwd():
    """Changes the current working directory "cwd" to the true path of where the user
    stores the contents of this program. Must keep the str ``shade``

    The ``/.../shade*/data/configurations.txt'' file will be shared throughout all executions,
    regardless of what path the user executes the program.

    This allows the user to make a:
     - keyboard shortcut (Unix and Windows may need a "macros" program to execute.
     - /usr/local/bin/shade executable (Linux and Unix).
     - alias in the ~/.bash_aliases or ~/.bash_profiles file (Linux and Unix).
    which can be called from any filepath directory. This function changes the "cwd" accordingly.

    [*] Note: ``shade*`` denotes the (optional) appended "-x.y.z" version number in
      the name, but cannot be renamed to anything NOT containing the substring 'shade'.
      Hence the GNU GPLv3 LICENSE.md

    Note: This function only needs to be called once (at the start of execution).

    """
    path_helper_py = os.path.realpath(__file__)
    if 'shade' not in path_helper_py:
        print(f'*** Critical failure ***\n'
              f'  This file is not located in any directory named `shade`.\n'
              f'  Please rename the package back to `shade` to continue.\n'
              f'  Feel free to keep the version number attached, e.g., `shade-0.1.2`\n'
              f'[Path]:  \'{path_helper_py}\'')
        sys.exit()

    temp_path = path_helper_py

    while 'shade' not in os.path.split(temp_path)[1]:
        # keep going one directory higher, i.e. "cd ..", until `shade` directory is found.
        temp_path = os.path.split(temp_path)[0]
    shade_dir_path = temp_path
    if os.getcwd() != shade_dir_path:
        print(f'Changing current working directory:\n'
              f' from: {os.getcwd()}')
        os.chdir(shade_dir_path)
        print(f'   to: {os.getcwd()}\n')


def get_data_path():
    # correct_cwd()
    return os.path.join(os.getcwd(), 'data')


def get_config_path():
    # correct_cwd()
    return os.path.join(get_data_path(), 'configurations.txt')


def data_dir_exists() -> bool:
    """Check to see if the ``/.../shade/data/`` directory exists
    and is a directory (not a file).

    Returns:
        True if it exists (as a directory), False otherwise.

    """
    return os.path.exists(get_data_path()) and os.path.isdir(get_data_path())


def config_file_exists() -> bool:
    """Check to see if the ``/.../shade/data/configurations.txt`` file exists
    and is a file (not a directory).

    Returns:
        True if it exists (as a file), False otherwise.

    """
    return os.path.exists(get_config_path()) and os.path.isfile(get_config_path())


def make_sure_data_dir_exists() -> bool:
    """Creates the ``/.../shade/data/`` directory if it does not already exist.

    Returns:
        True if it {starts, ends} with the data dir existing, False otherwise.

    TODO: once parse_args.py is finished:
          if data | configurations.txt is corrupt:
          resort to default config_dict.

    """
    if data_dir_exists():
        return True  # ``data`` already [1]: exists, [2]: is a directory

    # Error-checking: check if ``data`` is a file or anything-other-than a directory (link).
    if not os.path.exists(get_data_path()):
        pass  # 1st execution; no errors; create the dir
    elif os.path.isfile(get_data_path()):
        print('* Warning *\n'
              '/.../shade/data is a file, and not a directory as it should be.\n'
              'Attempting to remove the data file before proceeding.\n')
        try:
            os.remove(get_data_path())
            print('- Successfully removed the /../shade/data file.\n')
        except os.error as msg:
            print(f'*** Critical Error ***\n'
                  f'Failed to remove the file due to the Exception:\n'
                  f'  {msg}\n'
                  f'Please manually delete the data file to continue.\n'
                  f'[Path]:  \'{get_data_path()}\'\n')
            return False
    else:  # elif not os.path.isdir(get_data_path()):
        print(f'*** Critical Error ***\n'
              f'Unknown file type of data, and is not a directory as it should be.\n'
              f'Please manually delete `data` in order to continue.\n'
              f'[Path]:  \'{get_data_path()}\'\n')
        return False

    # By this point in the execution, the data directory path should not exist, therefore create it.
    if not os.path.exists(get_data_path()):
        os.mkdir(get_data_path())
        print(f'- Successfully created the data/ directory.\n'
              f'[Path]:  \'{get_data_path()}\'\n')
        return True  # just created

    print(f'``data`` was found to be of a non-directory filetype.\n'
          f'Please manually correct the deficiency in order\n'
          f'  to continue executing without this error.\n'
          f'[Path]:  \'{get_data_path()}\'\n')
    return False


def make_sure_config_file_exists() -> bool:
    """Creates the ``/.../shade/data/configurations.txt`` file if it does not already exist.

    Returns:
        True if it was just created, False if it already exists.

    TODO: once parse_args.py is finished:
          if data | configurations.txt is "corrupt":
          resort to default config_dict.

    """
    if not make_sure_data_dir_exists():
        # TODO: load default config_dict once parse_args.py is finished
        sys.exit()

    if config_file_exists():
        return True  # already created
    with open(get_config_path(), 'w'):
        # TODO: write defaults to file
        return True
