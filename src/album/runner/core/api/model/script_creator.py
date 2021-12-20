from abc import ABCMeta, abstractmethod

from album.runner.core.api.model.solution import ISolution


class IScriptCreator:
    """Interface for all ScriptCreator classes. Holds methods shared across all ScriptCreator classes."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_script(self, solution_object: ISolution, argv) -> str:
        """Creates the script with the execution_block of the concrete instance of the class"""
        raise NotImplementedError
