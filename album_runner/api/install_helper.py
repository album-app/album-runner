import os
import subprocess
from pathlib import Path

import requests

from album_runner import get_active_solution
from album_runner import logging

module_logger = logging.get_active_logger


class InstallError(Exception):
    """Exception class for argument extraction"""

    def __init__(self, short_message):
        self.short_message = short_message


def download_if_not_exists(active_solution, url, file_name):
    """Downloads resource if not already cached and returns local resource path.

    Args:
        active_solution: The solution object the download belongs to
        url: The URL of the download
        file_name: The local filename of the download

    Returns: The path to the downloaded resource

    """
    download_dir = active_solution.download_cache_path
    download_path = download_dir.joinpath(file_name)
    if download_path.exists():
        module_logger().info(f"Found cache of {url}: {download_path}...")
        return download_path
    if not download_dir.exists():
        download_dir.mkdir(parents=True)
    module_logger().info(f"Downloading {url} to {download_path}...")
    downloaded_obj = requests.get(url)

    with open(str(download_path), "wb") as file:
        file.write(downloaded_obj.content)
    return download_path


# todo: write test
def extract_tar(in_tar, out_dir):
    """

    Args:
        out_dir: Directory where the TAR file should be extracted to
        in_tar: TAR file to be extracted
    """
    import tarfile
    out_path = Path(out_dir)
    if not out_path.exists():
        out_path.mkdir(parents=True)
    module_logger().info(f"Extracting {in_tar} to {out_dir}...")
    my_tar = tarfile.open(in_tar)
    my_tar.extractall(out_dir)
    my_tar.close()


# todo: write test
def download_solution_repository(active_solution):
    """Downloads the repository specified in a solution object, returns repository_path on success.

    Additionally changes pythons working directory to the repository_path.

    Args:
        active_solution:
            The solution object.

    Returns:
        The directory of the git directory.

    """
    download_path = str(Path(active_solution["download_cache_path"]).joinpath(active_solution["name"]))

    r = subprocess.run(["git", "clone", active_solution['git_repo'], download_path])

    if r.returncode != 0:
        raise InstallError("Git clone operation failed! See logs for information!")

    # set python workdir
    os.chdir(download_path)

    return download_path


# todo: write test
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
