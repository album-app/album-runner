import sys

from album_runner.album_runner import AlbumRunner
from album_runner.logging import get_active_logger

"""
Global variable for tracking the currently active solution. Do not use this 
directly instead use get_active_solution()
"""
global _active_solution
_active_solution = []

enc = sys.getfilesystemencoding()
module_logger = logging.get_active_logger


def setup(**attrs):
    """This configures a solution for the use by the main album tool."""
    global _active_solution
    next_solution = AlbumRunner(attrs)
    push_active_solution(next_solution)


def album_runner_init(**attrs):
    active_solution = get_active_solution()
    for attr in attrs:
        if attr in AlbumRunner.api_keywords:
            # expects value to be a byte-str
            decoded_value = attrs[attr].decode(enc)
            setattr(active_solution, attr, decoded_value)


def push_active_solution(solution_object):
    """Pop a solution to the _active_solution stack."""
    global _active_solution
    _active_solution.insert(0, solution_object)


def get_parent_solution():
    """Return the parent solution of the currently active solution."""
    global _active_solution
    if len(_active_solution) > 1:
        return _active_solution[1]
    return None


def get_active_solution():
    """Return the currently active solution, which is defined globally."""
    global _active_solution
    if len(_active_solution) > 0:
        return _active_solution[0]
    return None


def pop_active_solution():
    """Pop the currently active solution from the _active_solution stack."""
    global _active_solution

    if len(_active_solution) > 0:
        return _active_solution.pop(0)
    else:
        return None
