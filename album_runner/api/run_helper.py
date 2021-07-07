import os
import subprocess
from pathlib import Path

from album_runner import logging, get_active_solution

module_logger = logging.get_active_logger


# todo: write test
def chdir_repository(path):
    """Actively changes pythons working directory to the cache path of the solution.

    Args:
        path:
            The path to change the working directory to.

    """
    # assumes repo is up to date!
    if Path(path).joinpath(".git").exists():
        os.chdir(path)
    else:
        raise FileNotFoundError("Could not identify %s as repository. Aborting..." % path)


# todo: write test
def add_dir_to_path(path):
    """Adds the given path to the pythonpath

    Args:
        path:
            The path to be added to the pythonpath.

    """
    import sys
    sys.path.insert(0, str(path))


def in_target_environment():
    """Gives the boolean information whether or not current python is the python from the album target environment.

    Returns:
        True when current active python is the album target environment else False.

    """
    import sys
    active_solution = get_active_solution()

    # todo: check whether this works in step-album
    return True if sys.executable.startswith(active_solution.environment_path) else False


# todo: write test
def run_as_executable(cmd, args):
    """Runs a solution as executable. Thereby only calling a command on the commandline within the correct environment.

    Args:
        cmd:
            The command to run.
        args:
            The arguments to the command.

    """
    from album.core import get_active_solution

    active_solution = get_active_solution()

    executable_path = active_solution.environment.path.joinpath("bin", cmd)
    cmd = [
        str(executable_path)
    ] + args

    subprocess.call(cmd)
