from abc import ABCMeta, abstractmethod


class ISolutionScript:

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_solution_script(self):
        raise NotImplementedError
