import unittest

from tests.unit.api import test_install_helper
from tests.unit.api import test_run_helper
from tests.unit import test_logging


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # ### unittests
    suite.addTests(loader.loadTestsFromModule(test_run_helper))
    suite.addTests(loader.loadTestsFromModule(test_install_helper))

    suite.addTests(loader.loadTestsFromModule(test_logging))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


main()
