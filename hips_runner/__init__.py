from hips_runner.hips_runner import HipsRunner
from hips_runner.logging import get_active_logger

"""
Global variable for tracking the currently active HIPS. Do not use this 
directly instead use get_active_hips()
"""
global _active_hips
_active_hips = []


module_logger = logging.get_active_logger


def setup(**attrs):
    """This configures a HIPS to for use by the main HIPS tool."""
    global _active_hips
    next_hips = HipsRunner(attrs)
    push_active_hips(next_hips)


def push_active_hips(hips_object):
    """Pop a hips to the _active_hips stack."""
    global _active_hips
    _active_hips.insert(0, hips_object)


def get_parent_hips():
    """Return the parent HIPS of the currently active HIPS."""
    global _active_hips
    if len(_active_hips) > 1:
        return _active_hips[1]
    return None


def get_active_hips():
    """Return the currently active HIPS, which is defined globally."""
    global _active_hips
    if len(_active_hips) > 0:
        return _active_hips[0]
    return None


def pop_active_hips():
    """Pop the currently active hips from the _active_hips stack."""
    global _active_hips

    if len(_active_hips) > 0:
        return _active_hips.pop(0)
    else:
        return None
