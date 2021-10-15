import sys
import tarfile
from pathlib import Path
from urllib.request import urlretrieve

from album.runner import logging, get_active_solution

module_logger = logging.get_active_logger


def download_if_not_exists(url, file_name):
    """Downloads resource if not already cached and returns local resource path.

    Args:
        url: The URL of the download.
        file_name: The local filename of the download.

    Returns: The path to the downloaded resource.

    """
    download_dir = get_cache_path()
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


# todo: extract_zip


def get_environment_name():
    """Returns the environment name the solution runs in."""
    active_solution = get_active_solution()

    return Path(active_solution.environment_name)


def get_environment_path():
    """Returns the path of the environment the solution runs in."""
    active_solution = get_active_solution()

    return Path(active_solution.environment_path)


def get_data_path():
    """Returns the data path provided for the solution."""
    active_solution = get_active_solution()

    return Path(active_solution.data_path)


def get_package_path():
    """Returns the package path provided for the solution."""
    active_solution = get_active_solution()

    return Path(active_solution.package_path)


def get_app_path():
    """Returns the app path provided for the solution."""
    active_solution = get_active_solution()

    return Path(active_solution.app_path)


def get_cache_path():
    """Returns the cache path provided for the solution."""
    active_solution = get_active_solution()

    return Path(active_solution.cache_path)


def in_target_environment():
    """Gives the boolean information whether or not current python is the python from the album target environment.

    Returns:
        True when current active python is the album target environment else False.

    """
    active_solution = get_active_solution()

    return True if sys.executable.startswith(
        active_solution["environment_path"]) else False


def get_args():
    """Get the parsed argument from the solution call.

    Returns:
        The namespace object of the parsed arguments.

    """
    active_solution = get_active_solution()

    return active_solution.args
