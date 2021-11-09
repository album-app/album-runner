class AlbumRunner:
    """Encapsulates a album solution."""

    setup_keywords = [
        'group', 'name', 'version', 'description', 'url', 'license',
        'min_album_version', 'tested_album_version', 'args',
        'init', 'run', 'install', 'uninstall', 'pre_test', 'test',
        'author', 'author_email',
        'long_description', 'git_repo', 'dependencies',
        'timestamp', 'format_version', 'authors', 'cite', 'tags',
        'documentation', 'covers', 'sample_inputs',
        'sample_outputs', 'doi', 'catalog', 'parent', 'steps', 'close', 'title'
    ]

    # CAUTION: deploy_keys also used for resolving. Make sure keys do not contain callable values.
    # If they do, add "to_string" method for @get_deploy_dict. Example see @_remove_action_from_args.
    deploy_keys = [
        'group', 'name', 'description', 'version', 'format_version', 'tested_album_version',
        'min_album_version', 'license', 'git_repo', 'authors', 'cite', 'tags', 'documentation',
        'covers', 'args', 'title', 'timestamp'
    ]

    api_keywords = ['environment_path', 'environment_name', 'cache_path', 'package_path', 'data_path', 'app_path']

    # default values
    group = None
    name = None
    min_album_version = None
    tested_album_version = None
    version = None
    dependencies = None
    parent = None
    doi = None

    args = []
    steps = []
    tags = []
    authors = []
    cite = ""

    # API keywords
    environment_path = None
    environment_name = None
    cache_path = None
    package_path = None
    data_path = None
    app_path = None

    # core keywords
    coordinates = None
    environment = None

    # lambdas
    init = None
    run = None
    install = None
    uninstall = None
    pre_test = None
    test = None

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

    def get_identifier(self):
        identifier = "_".join([self["group"], self["name"], self["version"]])
        return identifier
