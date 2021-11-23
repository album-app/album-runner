import unittest

from album.runner.model.solution import Solution


class TestAlbumRunner(unittest.TestCase):

    def test__init__(self):
        solution = Solution({"group": "testgroup", "name": "testname", "version": "testversion"})
        self.assertEqual("testgroup", solution.setup.group)
        self.assertEqual("testgroup", solution.setup["group"])
        solution.setup.group = "newvalue"
        self.assertEqual("newvalue", solution.setup.group)
        self.assertEqual("newvalue", solution.setup["group"])
