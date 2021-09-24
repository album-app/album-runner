import os
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.request import urlretrieve

from album_runner import logging, get_active_solution, AlbumRunner

module_logger = logging.get_active_logger


def download_if_not_exists(url, file_name):
    """Downloads resource if not already cached and returns local resource path.

    Args:
        url: The URL of the download
        file_name: The local filename of the download

    Returns: The path to the downloaded resource

    """
    active_solution = get_active_solution()

    download_dir = active_solution.download_cache_path
    download_path = download_dir.joinpath(file_name)

    if download_path.exists():
        module_logger().info(f"Found cache of {url}: {download_path}...")
        return download_path
    if not download_dir.exists():
        download_dir.mkdir(parents=True)

    module_logger().info(f"Downloading {url} to {download_path}...")

    urlretrieve(url, download_path)

    return download_path


def extract_tar(in_tar, out_dir):
    """

    Args:
        out_dir: Directory where the TAR file should be extracted to
        in_tar: TAR file to be extracted
    """
    out_path = Path(out_dir)

    if not out_path.exists():
        out_path.mkdir(parents=True)

    module_logger().info(f"Extracting {in_tar} to {out_dir}...")

    my_tar = tarfile.open(in_tar)
    my_tar.extractall(out_dir)
    my_tar.close()


def download_solution_repository():
    """Downloads the repository specified in a solution object, returns repository_path on success.

    Additionally changes pythons working directory to the repository_path.

    Returns:
        The directory of the git directory.

    """
    active_solution = get_active_solution()

    download_path = str(Path(active_solution["download_cache_path"]).joinpath(active_solution["name"]))

    r = subprocess.run(["git", "clone", active_solution['git_repo'], download_path])

    if r.returncode != 0:
        raise RuntimeError("Git clone operation failed! See logs for information!")

    # set python workdir
    os.chdir(download_path)

    return download_path


def install_package(module, version=None):
    """Installs a package in an environment.

    Args:
        module:
            The module name or a git like link. (e.g. "git+..." pip installation)
        version:
            The version of the package. If none, give, current latest is taken.

    """
    active_solution = get_active_solution()
    active_solution.environment.pip_install(module, version=version)


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

    return path


def add_dir_to_path(path):
    """Adds the given path to the pythonpath

    Args:
        path:
            The path to be added to the pythonpath.

    """
    sys.path.insert(0, str(path))


def in_target_environment():
    """Gives the boolean information whether or not current python is the python from the album target environment.

    Returns:
        True when current active python is the album target environment else False.

    """
    active_solution = get_active_solution()

    return True if sys.executable.startswith(active_solution["environment_path"]) else False


def run_as_executable(cmd, args):
    """Runs a solution as executable. Thereby only calling a command on the commandline within the correct environment.

    Args:
        cmd:
            The command to run.
        args:
            The arguments to the command.

    """
    active_solution = get_active_solution()

    executable_path = Path(active_solution["environment_path"]).joinpath("bin", cmd)
    cmd = [
              str(executable_path)
          ] + args

    subprocess.call(cmd)


def get_args():
    """Get the parsed argument from the solution call.

    Returns:
        The namespace object of the parsed arguments.

    """
    active_solution = get_active_solution()

    return active_solution.args
