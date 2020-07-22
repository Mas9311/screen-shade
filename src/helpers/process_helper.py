import os
import psutil
import sys


def kill_all_running_instances(run_py_filepath, verbose):
    """Terminates all instances of this program currently running. Does not ``restart`` the program.
    1: Retrieve all process ids of python currently running, and determine the .py file's path.
       - ``python3 ./prog/run.py --demo --verbose=2`` => ``/home/user2/Software/prog/run.py``
    2: One should be the current process, but if two are found, then user is requesting to terminate the other.
    3: If are two (2) instances of this program running at the same time,
       terminate the first (ordered by time of execution), then exit the currently-running program.
       - Note: all instances of this program will be terminated."""
    actual_file_path = os.path.abspath(run_py_filepath)
    pid = ''

    def _pid():
        return f'[pid {pid}]: '

    if verbose:
        print(f'Actual file path of shade\'s run.py: {actual_file_path}')

    # start: finding and filtering process
    pid_list = list(os.popen('pgrep python').read().strip().splitlines())
    if verbose:
        print(f' - Running python process ids: {pid_list}')

    instances = []
    for pid in pid_list:
        proc = psutil.Process(int(pid))
        if len(proc.cmdline()) > 1:
            cmdline_file_path = proc.cmdline()[1]
            if cmdline_file_path == actual_file_path:
                # User executed the program with full file path (explicit path execution).
                instances.append((pid, proc))
                continue

            # cmdline_file_path may include `./`, therefore may be an inaccurate filepath
            exec_file_name = os.path.basename(cmdline_file_path)  # looking for ``run.py``
            if exec_file_name not in actual_file_path:
                if verbose:
                    print(f'{_pid()}unrelated filename: {exec_file_name}.')
                    if verbose > 1:
                        print(f'{_pid()} > Skipped. Process not appended to running `instances` list.')
                continue

            if verbose:
                print(f'{_pid()}is running file: `{cmdline_file_path}`.')
            exec_path = os.path.abspath(exec_file_name)
            if verbose:
                print(f'{_pid()}Absolute filepath: {exec_path}')

            if not os.path.exists(exec_path):
                # Verbatim process filepath not immediately available.
                if verbose:
                    print(f'{_pid()} * Absolute filepath does not exist (like due to \'.\' in path.\n'
                          f'{_pid()}   - example executable: `./shade/run.py`\n'
                          f'{_pid()}  * Attempting to find absolute filepath.')
                manual_path = os.path.join(proc.cwd(), os.path.basename(cmdline_file_path))
                print(f'{_pid()} > Manually-constructed path: `{manual_path}`')
                if not os.path.exists(manual_path):
                    # filepath could not be determined
                    print(f'\n\n\n{_pid()}*** Fatal Error.\n'
                          f'{_pid()} > No known path for currently running python process:\n'
                          f'{_pid()}   - pid={pid}, name={os.path.basename(proc.cmdline()[1])}\n\n')
                    sys.exit()
                else:
                    # filepath recovered. Able to continue execution!
                    if verbose:
                        print(f'{_pid()} > Absolute filepath recovered: {manual_path}')
                    exec_path = manual_path

            if exec_path == actual_file_path:
                # Found an exact match.
                if verbose:
                    print(f'{_pid()}')
                    if verbose > 1:
                        print(f'{_pid()}   - instances[{len(instances)}] => Exec path: {exec_path}')
                instances.append((pid, proc))
            if verbose:
                print(end='\n')
    # Finished finding and filtering processes.

    # Determining course of action: {termination, continuation of execution}
    if len(instances) > 1:
        (pid, proc) = instances[0]  # grabs the first[0] instance. second[1] instance is current process.
        print(f'Two (2) running processes of this program found.\n'
              f' - Terminating the other open process.\n'
              f'   pid:{pid} cmdline=\'{proc.name()} {actual_file_path}\'')
        proc.terminate()  # os.kill(pid, signal.SIGTERM)  # on *nix: SIGTERM(-15), Windows: SIGKILL(-9)
        sys.exit()
    else:
        if verbose:
            print(f'Only 1 running instance found of this program; continuing execution.\n')
