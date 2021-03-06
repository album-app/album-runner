from album.runner.core.model.coordinates import Coordinates

from tests.test_unit_common import TestUnitCommon


class TestCoordinates(TestUnitCommon):

    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test__init__(self):
        x = Coordinates("a", "b", "c")

        self.assertEqual(x._group, "a")
        self.assertEqual(x._name, "b")
        self.assertEqual(x._version, "c")

    def test_group(self):
        x = Coordinates("a", "B", "c")

        self.assertEqual("a", x.group())

    def test_name(self):
        x = Coordinates("a", "B", "c")

        self.assertEqual("B", x.name())

    def test_version(self):
        x = Coordinates("a", "B", "c")

        self.assertEqual("c", x.version())

    def test__str__(self):
        x = Coordinates("a", "B", "c")

        self.assertEqual("a:B:c", str(x))

    def test__eq__(self):
        x = Coordinates("a", "B", "c")
        y = Coordinates("x", "Y", "z")
        z = Coordinates("a", "b", "c")
        w = Coordinates("a", "B", "c")

        self.assertFalse(x == y)
        self.assertFalse(x == z)
        self.assertFalse(z == x)  # test transitivity
        self.assertTrue(x == w)  # positive test-space
