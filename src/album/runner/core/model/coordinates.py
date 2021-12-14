from album.runner.core.api.model.coordinates import ICoordinates


class Coordinates(ICoordinates):
    """Class for the Coordinates of a solution."""

    def __init__(self, group: str, name: str, version: str) -> None:
        self._group = group
        self._name = name
        self._version = version


    def name(self):
        return self._name

    def group(self):
        return self._group

    def version(self):
        return self._version

    def __str__(self) -> str:
        return f"{self._group}:{self._name}:{self._version}"

    def __eq__(self, o: object) -> bool:
        return isinstance(
            o, ICoordinates
        ) and o.group() == self._group and o.name() == self._name and o.version() == self._version

    def __hash__(self):
        return hash(self.__str__())
