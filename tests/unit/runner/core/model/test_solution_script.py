import unittest

from album.runner.core.model.solution_script import SolutionScript
from tests.test_unit_common import TestUnitCommon


class TestSolutionScript(TestUnitCommon):

    @unittest.skip("Needs to be implemented!")
    def test__init__(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test_create_solution_script(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__create_header(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__create_body(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__api_access(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__append_arguments(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__handle_args_string(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__handle_args_list(self):
        # ToDo: implement
        pass

    def test__create_parser_argument_string(self):
        args = {
            'name': 'myname'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', )\n', res)

        args = {
            'name': 'myname',
            'type': 'integer'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', type=int, )\n', res)

        args = {
            'name': 'myname',
            'type': 'boolean'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', type=strtobool, )\n', res)

        args = {
            'name': 'myname',
            'type': 'string'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', type=str, )\n', res)

        args = {
            'name': 'myname',
            'type': 'file'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', type=Path, )\n', res)

        args = {
            'name': 'myname',
            'type': 'directory'
        }
        res = SolutionScript._create_parser_argument_string(args)
        self.assertEqual('parser.add_argument(\'--myname\', type=Path, )\n', res)

    @unittest.skip("Needs to be implemented!")
    def test__create_action_class_string(self):
        # ToDo: implement
        pass

    @unittest.skip("Needs to be implemented!")
    def test__get_action_class_name(self):
        # ToDo: implement
        pass
