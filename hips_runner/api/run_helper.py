import os
import subprocess
from pathlib import Path

from hips_runner import logging, get_active_hips

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
def run_as_executable(cmd, args):
    """Runs a solution as executable. Thereby only calling a command on the commandline within the correct environment.

    Args:
        cmd:
            The command to run.
        args:
            The arguments to the command.

    """
    from hips.core import get_active_hips

    active_hips = get_active_hips()

    executable_path = active_hips.environment.path.joinpath("bin", cmd)
    cmd = [
        str(executable_path)
    ] + args

    subcommand.run(cmd)