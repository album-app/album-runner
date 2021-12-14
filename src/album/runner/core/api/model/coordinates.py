from abc import ABCMeta, abstractmethod


class ICoordinates:

    __metaclass__ = ABCMeta

    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def group(self):
        raise NotImplementedError

    @abstractmethod
    def version(self):
        raise NotImplementedError