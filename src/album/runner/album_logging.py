import logging
import threading
from enum import Enum, unique

"""
Global variable for tracking the currently active logger. Do not use this
directly instead use get_active_logger()
"""
_active_logger = {}

DEBUG = False


def thread_stack():
    global _active_logger
    thread_id = threading.current_thread().ident
    if thread_id not in _active_logger:
        _active_logger[thread_id] = []
    return _active_logger.get(thread_id)


def push_active_logger(logger):
    """Insert a logger to the _active_logger stack."""
    thread_stack().insert(0, logger)


def get_active_logger():
    """Return the currently active logger, which is defined globally."""
    stack = thread_stack()
    if len(stack) > 0:
        return stack[0]
    return logging.getLogger()  # root logger


def get_active_logger_in_thread(thread_ident):
    """Return the currently active logger, which is defined globally."""
    if thread_ident in _active_logger:
        stack = _active_logger.get(thread_ident)
        if len(stack) > 0:
            return stack[0]
    return logging.getLogger()  # root logger


def pop_active_logger():
    """Pop the currently active logger from the _active_solution stack."""

    stack = thread_stack()
    if len(stack) > 0:
        logger = stack.pop(0)
        logger.handlers.clear()
        return logger
    else:
        return logging.getLogger()  # root logger


@unique
class LogLevel(Enum):
    """LogLevel album allows.

    Notes:
        Only add Names available in python standard logging module.

    """
    DEBUG = 1
    INFO = 0
    WARNING = 2
    ERROR = 3


def to_loglevel(value):
    """Converts a string value to a @LogLevel.

    Args:
        value:
            The string value

    Returns:
        The LovLevel class enum

    Raises:
        KeyError when loglevel unknown.

    """
    try:
        return LogLevel[value]
    except KeyError as err:
        logger = get_active_logger()
        logger.error('Loglevel %s not allowed or unknown!' % value)
        raise err


def configure_logging(name, loglevel=None, stream_handler=None, formatter_string=None, parent_thread_id=None,
                      parent_name=None):
    """Configures a logger with a certain name and loglevel.

        loglevel:
            The Loglevel to use. Either DEBUG or INFO.
        name:
            The name of the logger.

    Returns:
        The logger object.

    """
    # create or get currently active logger
    if parent_thread_id is None:
        parent = get_active_logger()
    else:
        parent = get_active_logger_in_thread(parent_thread_id)

    if not parent_name:
        parent_name = parent.name

    # if currently active logger has the same name, just return it
    if parent_name == name:
        return parent

    # make sure the new logger is registered as a child of the currently active logger in order to propagate logs
    if parent_name.endswith("." + name):
        name = parent_name
    else:
        if not name.startswith(parent_name + "."):
            name = parent_name + "." + name

    logger = logging.getLogger(name)
    if loglevel is None:
        logger.setLevel(parent.level)
    else:
        logger.setLevel(loglevel.name)

    if stream_handler:
        # create formatter
        if not formatter_string:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            formatter = logging.Formatter(formatter_string)
        # create console handler and set level to debug
        # ToDo: different handlers necessary? e.g. logging additional into a file?
        ch = logging.StreamHandler(stream_handler)
        ch.setLevel(loglevel.name)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # push logger if not already active
    if get_active_logger() != logger:
        push_active_logger(logger)

    return logger


def get_loglevel():
    """Returns the loglevel of the current active logger."""
    return get_active_logger().level


def get_loglevel_name():
    """Returns the Name of the loglevel of the current active logger."""
    logger = get_active_logger()
    return logging.getLevelName(logger.level)


def set_loglevel(loglevel):
    """ Sets logLevel for a logger with a certain name for ALL available handlers.

    Args:
        loglevel:
            The Loglevel to use. Either DEBUG or INFO.

    """
    # logger loglevel
    active_logger = get_active_logger()
    active_logger.debug('Set loglevel to %s...' % loglevel.name)

    active_logger.setLevel(loglevel.name)

    # set handler loglevel
    for handler in active_logger.handlers:
        handler_name = handler.stream.name if hasattr(handler, "stream") and hasattr(handler.stream,
                                                                                     active_logger.name) else "default handler"
        active_logger.debug('Set loglevel for handler %s to %s...' % (handler_name, loglevel.name))
        handler.setLevel(loglevel.name)


class LogEntry:
    name = None
    level = None
    message = None

    def __init__(self, name, level, message):
        self.name = name
        self.level = level
        self.message = message


def debug_settings():
    return DEBUG
