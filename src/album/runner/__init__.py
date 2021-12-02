import sys
from typing import Optional

from album.runner.model.solution import Solution
from album.runner.album_logging import get_active_logger

"""
Global variable for tracking the currently active solution. Do not use this 
directly instead use get_active_solution()
"""
_active_solution = []

enc = sys.getfilesystemencoding()


def setup(**attrs):
    """This configures a solution for the use by the main album tool."""
    global _active_solution
    next_solution = Solution(attrs)
    push_active_solution(next_solution)


def album_runner_init(**attrs):
    active_solution = get_active_solution()
    for attr in attrs:
        if attr in active_solution.installation.__dict__:
            # expects value to be a byte-str
            decoded_value = attrs[attr].decode(enc)
            setattr(active_solution.installation, attr, decoded_value)

    # add app_path to syspath
    sys.path.insert(0, active_solution.installation.app_path)


def push_active_solution(solution_object: Solution):
    """Pop a solution to the _active_solution stack."""
    global _active_solution
    _active_solution.insert(0, solution_object)


def get_parent_solution() -> Optional[Solution]:
    """Return the parent solution of the currently active solution."""
    global _active_solution
    if len(_active_solution) > 1:
        return _active_solution[1]
    return None


def get_active_solution() -> Optional[Solution]:
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
