import logging
import re
from io import StringIO

from album.runner.core.api.model.solution_script import ISolutionScript

from tests.test_unit_common import TestUnitCommon


class TestSolutionScript(TestUnitCommon):

    def test_get_script_logging_formatter_str_regex(self):
        logger = logging.getLogger('test')
        logger.setLevel('INFO')
        formatter = logging.Formatter(ISolutionScript.get_script_logging_formatter_str())
        capture = StringIO()
        ch = logging.StreamHandler(capture)
        ch.setFormatter(formatter)
        ch.setLevel('INFO')
        logger.addHandler(ch)
        logger.info('a message')
        logger.error('an error')
        logs = capture.getvalue().strip().split('\n')
        self.assertEqual(2, len(logs))
        r = re.search(ISolutionScript.get_script_logging_formatter_regex(), logs[0])
        self.assertEqual('INFO', r.group(1))
        self.assertEqual('test', r.group(2))
        self.assertEqual('a message', r.group(3))
        r = re.search(ISolutionScript.get_script_logging_formatter_regex(), logs[1])
        self.assertEqual('ERROR', r.group(1))
        self.assertEqual('test', r.group(2))
        self.assertEqual('an error', r.group(3))
