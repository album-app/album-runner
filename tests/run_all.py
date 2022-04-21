import time
import unittest

from tests.integration import test_integration_script_creator
from tests.unit.runner import test_album_logging, test_api
from tests.unit.runner.core.model import test_solution, test_coordinates, test_script_creator, test_solution_script


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # ### unittests

    # runner
    suite.addTests(loader.loadTestsFromModule(test_api))
    suite.addTests(loader.loadTestsFromModule(test_album_logging))
    # core model
    suite.addTests(loader.loadTestsFromModule(test_solution))
    suite.addTests(loader.loadTestsFromModule(test_coordinates))
    suite.addTests(loader.loadTestsFromModule(test_script_creator))
    suite.addTests(loader.loadTestsFromModule(test_solution_script))

    # integration tests
    suite.addTests(loader.loadTestsFromModule(test_integration_script_creator))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
    if result.wasSuccessful():
        time.sleep(10)
        print("Success")
        exit(0)
    else:
        print("Failed")
        exit(1)


main()
