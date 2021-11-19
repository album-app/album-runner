class AlbumRunner:
    """Encapsulates a album solution."""

    setup_keywords = [
        # identity - mandatory
        'group', 'name', 'version',
        # lambdas
        'init', 'run', 'install', 'uninstall', 'pre_test', 'test', 'close',
        # dependencies
        'parent',  'steps',
        # others
        'description', 'url', 'license', 'album_version', 'album_api_version', 'args',
        'author', 'author_email', 'git_repo', 'dependencies',
        'timestamp', 'authors', 'cite', 'tags', 'contact',
        'documentation', 'covers', 'doi', 'catalog', 'title', 'acknowledgement'
    ]

    # CAUTION: deploy_keys also used for resolving. Make sure keys do not contain callable values.
    # If they do, add "to_string" method for @get_deploy_dict. Example see @_remove_action_from_args.
    deploy_keys = [
        'group', 'name', 'description', 'version', 'album_api_version',
        'album_version', 'license', 'git_repo', 'authors', 'cite', 'tags', 'documentation',
        'covers', 'args', 'title', 'timestamp'
    ]

    api_keywords = ['environment_path', 'environment_name', 'cache_path', 'package_path', 'data_path', 'app_path']

    # lambdas
    init = None
    run = None
    install = None
    uninstall = None
    pre_test = None
    test = None
    close = None

    # solution metadata
    group = None
    name = None
    version = None
    dependencies = None
    parent = None
    doi = None
    title = None
    license = None
    git_repo = None
    acknowledgement = None

    args = []
    steps = []
    tags = []
    authors = []
    cite = []
    description = []

    # framework metadata
    album_version = None
    album_api_version = None

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
