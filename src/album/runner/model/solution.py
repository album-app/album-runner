from album.runner.model.coordinates import Coordinates


class Solution:
    """Encapsulates a album solution configuration."""

    class Setup(dict):
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

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

    class Installation:
        def __init__(self):
            super().__init__()
            # API keywords
            self.environment_path = None
            self.environment_name = None
            self.user_cache_path = None
            self.internal_cache_path = None
            self.package_path = None
            self.data_path = None
            self.app_path = None

    def __init__(self, attrs=None):
        self.installation = Solution.Installation()
        self.setup = Solution.Setup(attrs)
        self.coordinates = Coordinates(attrs['group'], attrs['name'], attrs['version'])
        self.args = None
        self.script = None

    def get_arg(self, k):
        """Get a specific named argument for this album if it exists."""
        matches = [arg for arg in self.setup.args if arg['name'] == k]
        return matches[0]

    def get_identifier(self):
        identifier = '_'.join([self.setup.group, self.setup.name, self.setup.version])
        return identifier

    def __eq__(self, other):
        return isinstance(other, Solution) and \
               other.coordinates == self.coordinates
