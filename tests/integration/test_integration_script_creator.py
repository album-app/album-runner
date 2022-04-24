import unittest

from album.runner.api import get_args, get_active_solution, pop_active_solution
from album.runner.core.model.script_creator import ScriptCreatorRun, ScriptCreatorTest
from tests.test_unit_common import TestUnitCommon


class TestIntegrationScriptCreator(TestUnitCommon):

    def test_get_args(self):

        solution_content = """
from album.runner.api import setup

setup(**{
            'group': "tsg",
            'name': "tsn",
            'version': "tsv",
            'args': [{"name": "a1", "description": ""}]
        })
"""
        exec(solution_content)
        active_solution = get_active_solution()
        active_solution.set_script(solution_content)
        pop_active_solution()
        creator = ScriptCreatorRun()

        # test no arg
        script = creator.create_script(active_solution, [''])
        exec(script)
        args = get_args()
        self.assertIsNone(args.a1)

        # test with arg
        script = creator.create_script(active_solution, ['', '--a1', 'aValue'])
        exec(script)
        args = get_args()
        self.assertEqual('aValue', args.a1)

    def test_test_without_pretest(self):

        solution_content = """
from album.runner.api import setup

setup(**{
            'group': "tsg",
            'name': "tsn",
            'version': "tsv",
            'test': lambda: True,
            'args': [{"name": "a1", "description": ""}]
        })
"""
        exec(solution_content)
        active_solution = get_active_solution()
        active_solution.set_script(solution_content)
        pop_active_solution()
        creator = ScriptCreatorTest()

        script = creator.create_script(active_solution, [''])
        exec(script)

    def test_test_pretest_without_return(self):

        solution_content = """
from album.runner.api import setup

def pre_test():
    print("jej")

setup(**{
            'group': "tsg",
            'name': "tsn",
            'version': "tsv",
            'pre_test': pre_test,
            'test': lambda: True,
            'args': [{"name": "a1", "description": ""}]
        })
"""
        exec(solution_content)
        active_solution = get_active_solution()
        active_solution.set_script(solution_content)
        pop_active_solution()
        creator = ScriptCreatorTest()

        script = creator.create_script(active_solution, [''])
        exec(script)


if __name__ == '__main__':
    unittest.main()
