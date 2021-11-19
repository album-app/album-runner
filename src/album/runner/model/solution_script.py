import json
import sys
from argparse import ArgumentError

from album.runner import AlbumRunner, album_logging

module_logger = album_logging.get_active_logger
enc = sys.getfilesystemencoding()


class SolutionScript:
    def __init__(self, solution_object: AlbumRunner, execution_block, argv):
        self.solution_object = solution_object
        self.execution_block = execution_block
        self.argv = argv

    def create_solution_script(self):
        script = self._create_header()
        script += self._create_body()
        script += self.execution_block

        return script

    def _create_header(self):
        header = (
            "import sys\n"
            "import json\n"
            "import argparse\n"
            "from album.runner import *\n"
            "from album.runner.album_logging import configure_logging, LogLevel, get_active_logger\n"
            "module_logger = get_active_logger\n"
        )
        # create logging
        parent_name = album_logging.get_active_logger().name
        header += "configure_logging(\"%s\", loglevel=%s, stream_handler=sys.stdout, " % (
            self.solution_object['name'], album_logging.to_loglevel(album_logging.get_loglevel_name())
        ) + "formatter_string=\"" + r"%(name)s - %(levelname)s - %(message)s" + "\", parent_name=\"%s\")\n" % parent_name
        header += "print = module_logger().info\n"
        # This could have an issue with nested quotes
        module_logger().debug("Add sys.argv arguments to runtime script: %s..." % ", ".join(self.argv))
        header += "sys.argv = json.loads(r'%s')\n" % json.dumps(self.argv)

        return header

    def _create_body(self):
        # add the album script
        script = self.solution_object['script']
        # init routine
        # script += "\nget_active_solution().init()\n" THIS FEATURE IS TEMPORARY DISABLED
        # API access
        script += self._api_access()

        script += self._append_arguments(self.solution_object['args'])
        return script

    def _api_access(self):
        # mapping from internal paths to API paths for the user
        script = "album_runner_init("
        script += "environment_path=" + "{}".format(str(self.solution_object.environment.path).encode(enc)) + ", "
        script += "environment_name=" + "{}".format(str(self.solution_object.environment.name).encode(enc)) + ", "
        script += "data_path=" + "{}".format(str(self.solution_object.data_path).encode(enc)) + ", "
        script += "package_path=" + "{}".format(str(self.solution_object.package_path).encode(enc)) + ", "
        script += "app_path=" + "{}".format(str(self.solution_object.app_path).encode(enc)) + ", "
        script += "cache_path=" + "{}".format(str(self.solution_object.cache_path).encode(enc))
        script += ")\n"
        return script

    def _append_arguments(self, args):
        script = ""
        module_logger().debug(
            'Read out arguments in album solution and add to runtime script...')
        # special argument parsing cases
        if isinstance(args, str):
            self._handle_args_string(args)
        else:
            script += self._handle_args_list(args)
        return script

    @staticmethod
    def _handle_args_string(args):
        # pass through to module
        if args == 'pass-through':
            module_logger().info(
                'Argument parsing not specified in album solution. Passing arguments through...'
            )
        else:
            message = 'Argument keyword \'%s\' not supported!' % args
            module_logger().error(message)
            raise ArgumentError(message)

    def _handle_args_list(self, args):
        module_logger().debug('Add argument parsing for album solution to runtime script...')
        # Add the argument handling
        script = "\nparser = argparse.ArgumentParser(description='Album Run %s')\n" % self.solution_object['name']
        for arg in args:
            if 'action' in arg.keys():
                script += self._create_action_class_string(arg)
            script += self._create_parser_argument_string(arg)
        script += "\nget_active_solution().args = parser.parse_args()\n"
        return script

    def _create_parser_argument_string(self, arg):
        keys = arg.keys()

        if 'default' in keys and 'action' in keys:
            module_logger().warning("Default values cannot be automatically set when an action is provided! "
                                    "Ignoring default values...")

        parse_arg = "parser.add_argument('--%s', " % arg['name']
        if 'default' in keys:
            parse_arg += "default='%s', " % arg['default']
        if 'description' in keys:
            parse_arg += "help='%s', " % arg['description']
        if 'required' in keys:
            parse_arg += "required=%s, " % arg['required']  # CAUTION: no ''! Boolean value
        if 'action' in keys:
            class_name = self._get_action_class_name(arg['name'])
            parse_arg += "action=%s, " % class_name  # CAUTION: no ''! action must be callable!
        parse_arg += ")\n"

        return parse_arg

    def _create_action_class_string(self, arg):
        class_name = self._get_action_class_name(arg['name'])
        return """
class {class_name}(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super({class_name}, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, get_active_solution().get_arg(self.dest)['action'](values))

""".format(class_name=class_name)

    @staticmethod
    def _get_action_class_name(name):
        class_name = '%sAction' % name.capitalize()
        return class_name