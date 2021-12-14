import unittest

from album.runner.core.model.solution import Solution


class TestAlbumRunner(unittest.TestCase):

    def test__init__(self):
        solution = Solution({"group": "testgroup", "name": "testname", "version": "testversion"})
        self.assertEqual("testgroup", solution._setup.group)
        self.assertEqual("testgroup", solution._setup["group"])
        solution._setup.group = "newvalue"
        self.assertEqual("newvalue", solution._setup.group)
        self.assertEqual("newvalue", solution._setup["group"])
        solution.set_args(["a", "b"])
        self.assertEqual(["a", "b"], solution.args())
