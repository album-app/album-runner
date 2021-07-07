import unittest
from io import StringIO

from album_runner.logging import *


def helper_test_configure_logging(logger):
    handler_levels = []
    for handler in logger.handlers:
        handler_levels.append(logging.getLevelName(handler.level))

    return handler_levels


class TestLogging(unittest.TestCase):

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
            logger = configure_logging(level, "test_%s" % idx)

            self.assertTrue(logging.getLevelName(logger.level) == level.name)

            handler_levels = helper_test_configure_logging(logger)
            self.assertEqual(handler_levels, [level.name] * len(handler_levels))

    def test_configure_logging_twice(self):
        logger = configure_logging(self.loglevels[0], "test_logger")
        self.assertEqual(get_active_logger(), logger)
        logger2 = configure_logging(self.loglevels[0], "test_logger")
        self.assertEqual(logger, logger2)
        self.assertEqual(get_active_logger(), logger)
        self.assertEqual(pop_active_logger(), logger)
        self.assertEqual(pop_active_logger(), logging.getLogger())  # this should be the root logger

    def test_set_loglevel(self):
        init_level = LogLevel(0)
        to_level = LogLevel(1)

        # init logger and check if logging level OK
        logger = configure_logging(init_level, "test")
        self.assertTrue(logging.getLevelName(logger.level) == init_level.name)

        handler_levels = helper_test_configure_logging(logger)
        self.assertEqual(handler_levels, [init_level.name] * len(handler_levels))

        # switch level and check if OK for logger and all logger.handler
        set_loglevel(to_level)

        self.assertTrue(logging.getLevelName(logger.level) == to_level.name)

        handler_levels = helper_test_configure_logging(logger)
        self.assertEqual(handler_levels, [to_level.name] * len(handler_levels))


class TestLogfileBuffer(unittest.TestCase):
    def setUp(self) -> None:
        self.capture_output = StringIO()
        self.configure_test_logging(self.capture_output)

    def tearDown(self) -> None:
        pop_active_logger()
        super().tearDown()

    def test_write(self):

        self.assertIsNotNone(get_active_logger())

        log_buffer = LogfileBuffer()
        log_buffer.write("WARNING - message\n over \n several \n lines")

        logs = self.get_logs()
        self.assertIn("WARNING - message", logs[0])
        self.assertEqual("\t\tover", logs[1])
        self.assertEqual("\t\tseveral", logs[2])
        self.assertEqual("\t\tlines", logs[3])

    def test_write_with_loglevel(self):

        self.assertIsNotNone(get_active_logger())

        log_buffer = LogfileBuffer()
        log_buffer.write("app1 - WARNING - message\n over \n several \n lines\napp1 - INFO - i\no\ns\nl")

        logs = self.get_logs()
        self.assertIn("app1 - WARNING - message", logs[0])
        self.assertEqual("\t\tover", logs[1])
        self.assertEqual("\t\tseveral", logs[2])
        self.assertEqual("\t\tlines", logs[3])
        self.assertIn("app1 - INFO - i", logs[4])
        self.assertEqual("\t\to", logs[5])
        self.assertEqual("\t\ts", logs[6])
        self.assertEqual("\t\tl", logs[7])

    def configure_test_logging(self, stream_handler):
        self.logger = logging.getLogger("unitTest")

        if not self.logger.hasHandlers():
            self.logger.setLevel('INFO')
            ch = logging.StreamHandler(stream_handler)
            ch.setLevel('INFO')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            push_active_logger(self.logger)

    def get_logs(self):
        logs = self.capture_output.getvalue()
        logs = logs.strip()
        return logs.split("\n")


if __name__ == '__main__':
    unittest.main()
