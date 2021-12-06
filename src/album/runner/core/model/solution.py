from pathlib import Path
from typing import List

from album.runner.core.api.model.solution import ISolution
from album.runner.core.api.model.coordinates import ICoordinates
from album.runner.core.model.coordinates import Coordinates


class Solution(ISolution):
    """Encapsulates a album solution configuration."""

    class Setup(ISolution.ISetup):

        def __init__(self, attrs=None):
            """sets object attributes

            Args:
                attrs:
                    Dictionary containing the attributes.
            """
            if attrs:
                super().__init__(attrs)
            else:
                super().__init__()

        def __str__(self, indent=2):
            s = '\n'
            for attr in self.__dict__:
                for i in range(0, indent):
                    s += '\t'
                s += (attr + ':\t' + str(getattr(self, attr))) + '\n'
            return s

    class Installation (ISolution.IInstallation):
        def __init__(self):
            super().__init__()
            # API keywords
            self._environment_path = None
            self._environment_name = None
            self._user_cache_path = None
            self._internal_cache_path = None
            self._package_path = None
            self._data_path = None
            self._app_path = None

        def environment_path(self) -> Path:
            return self._environment_path

        def environment_name(self) -> str:
            return self._environment_name

        def user_cache_path(self) -> Path:
            return self._user_cache_path

        def internal_cache_path(self) -> Path:
            return self._internal_cache_path

        def package_path(self) -> Path:
            return self._package_path

        def data_path(self) -> Path:
            return self._data_path

        def app_path(self) -> Path:
            return self._app_path

        def set_environment_path(self, path: Path):
            self._environment_path = path

        def set_environment_name(self, name: str):
            self._environment_name = name

        def set_user_cache_path(self, user_cache_path: Path):
            self._user_cache_path = user_cache_path

        def set_internal_cache_path(self, internal_cache_path: Path):
            self._internal_cache_path = internal_cache_path

        def set_package_path(self, package_path: Path):
            self._package_path = package_path

        def set_data_path(self, data_path: Path):
            self._data_path = data_path

        def set_app_path(self, app_path: Path):
            self._app_path = app_path

    def __init__(self, attrs=None):
        self._installation = Solution.Installation()
        self._setup = Solution.Setup(attrs)
        self._coordinates = Coordinates(attrs['group'], attrs['name'], attrs['version'])
        self._args = None
        self._script = None

    def setup(self) -> ISolution.ISetup:
        return self._setup

    def installation(self) -> ISolution.IInstallation:
        return self._installation

    def coordinates(self) -> ICoordinates:
        return self._coordinates

    def script(self) -> str:
        return self._script

    def get_arg(self, k):
        """Get a specific named argument for this album if it exists."""
        matches = [arg for arg in self._setup.args if arg['name'] == k]
        return matches[0]

    def get_identifier(self) -> str:
        identifier = '_'.join([self._setup.group, self._setup.name, self._setup.version])
        return identifier

    def set_script(self, script: str):
        self._script = script

    def __eq__(self, other):
        return isinstance(other, Solution) and \
               other.coordinates() == self._coordinates

    def set_args(self, args: List):
        self._args = args

    def args(self) -> List:
        return self._args
