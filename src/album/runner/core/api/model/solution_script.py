from abc import ABCMeta, abstractmethod


class ISolutionScript:

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_solution_script(self):
        raise NotImplementedError

    @staticmethod
    def get_script_logging_formatter_str():
        return '%(levelname)-7s %(name)s - %(message)s'

    @staticmethod
    def get_script_logging_formatter_regex():
        regex_log_level = 'DEBUG|INFO|WARNING|ERROR'
        return r'(%s)\s+([\s\S]+) - ([\s\S]+)?' % regex_log_level
