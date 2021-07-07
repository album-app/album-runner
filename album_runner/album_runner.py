class AlbumRunner:
    """Encapsulates a album solution."""

    setup_keywords = ('group', 'name', 'version', 'description', 'url', 'license',
                      'min_album_version', 'tested_album_version', 'args',
                      'init', 'run', 'install', 'pre_test', 'test', 'author', 'author_email',
                      'long_description', 'git_repo', 'dependencies',
                      'timestamp', 'format_version', 'authors', 'cite', 'tags',
                      'documentation', 'covers', 'sample_inputs',
                      'sample_outputs', 'doi', 'catalog', 'parent', 'steps', 'close', 'title')

    api_keywords = ('environment_path', 'environment_name', 'environment_cache_path', 'download_cache_path')

    # default values
    dependencies = None
    parent = None

    def __init__(self, attrs=None):
        """sets object attributes in setup_keywords

        Args:
            attrs:
                Dictionary containing the attributes.
        """
        # Attributes from the solution.py
        for attr in self.setup_keywords:
            if attr in attrs:
                setattr(self, attr, attrs[attr])

    def __str__(self, indent=2):
        s = '\n'
        for attr in self.setup_keywords:
            if attr in dir(self):
                for ident in range(0, indent):
                    s += '\t'
                s += (attr + ':\t' + str(getattr(self, attr))) + '\n'
        return s

    def __getitem__(self, k):
        if hasattr(self, k):
            return getattr(self, k)
        return None

    def get_arg(self, k):
        """Get a specific named argument for this album if it exists."""
        matches = [arg for arg in self['args'] if arg['name'] == k]
        return matches[0]
