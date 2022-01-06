import logging

from album.runner.album_logging import configure_logging, get_active_logger, LogLevel, pop_active_logger, to_loglevel, \
    set_loglevel, LogEntry
from tests.test_unit_common import TestUnitCommon


def helper_test_configure_logging(logger):
    handler_levels = []
    for handler in logger.handlers:
        handler_levels.append(logging.getLevelName(handler.level))

    return handler_levels


class TestAlbumLogging(TestUnitCommon):

    def tearDown(self) -> None:
        while True:
            logger = pop_active_logger()
            if logger == logging.getLogger():
                break

    def setUp(self):
        # all logging levels
        self.loglevels = [LogLevel(0), LogLevel(1)]

    def test_to_loglevel(self):

        for level in self.loglevels:
            self.assertEqual(to_loglevel(level.name), level)

        with self.assertRaises(KeyError):
            to_loglevel("NotAvailableLogLevel")

    def test_configure_logging(self):
        for idx, level in enumerate(self.loglevels):
            # set correct logging level for logger and all logger.handler for all logging level
            logger = configure_logging("test_%s" % idx, loglevel=level)

            self.assertTrue(logging.getLevelName(logger.level) == level.name)

            handler_levels = helper_test_configure_logging(logger)
            self.assertEqual(handler_levels, [level.name] * len(handler_levels))

    def test_configure_logging_twice(self):
        logger = configure_logging("test_logger", loglevel=self.loglevels[0])
        self.assertEqual(get_active_logger(), logger)
        logger2 = configure_logging(logger.name, loglevel=self.loglevels[0])
        self.assertEqual(logger, logger2)
        self.assertEqual(get_active_logger(), logger)
        self.assertEqual(pop_active_logger(), logger)
        self.assertEqual(pop_active_logger(), logging.getLogger())  # this should be the root logger

    def test_set_loglevel(self):
        init_level = LogLevel(0)
        to_level = LogLevel(1)

        # init logger and check if logging level OK
        logger = configure_logging("test", loglevel=init_level)
        self.assertEqual(logging.getLevelName(logger.level), init_level.name)

        handler_levels = helper_test_configure_logging(logger)
        self.assertEqual(handler_levels, [init_level.name] * len(handler_levels))

        # switch level and check if OK for logger and all logger.handler
        set_loglevel(to_level)

        self.assertTrue(logging.getLevelName(logger.level) == to_level.name)

        handler_levels = helper_test_configure_logging(logger)
        self.assertEqual(handler_levels, [to_level.name] * len(handler_levels))


class TestLogEntry(TestUnitCommon):
    def test__init__(self):
        log_entry = LogEntry("n", "l", "m")

        self.assertEqual("n", log_entry.name)
        self.assertEqual("l", log_entry.level)
        self.assertEqual("m", log_entry.message)

