import unittest


from tests.unit import test_logging, test_api, test_album_runner


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # ### unittests
    suite.addTests(loader.loadTestsFromModule(test_api))
    suite.addTests(loader.loadTestsFromModule(test_album_runner))
    suite.addTests(loader.loadTestsFromModule(test_logging))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


main()
