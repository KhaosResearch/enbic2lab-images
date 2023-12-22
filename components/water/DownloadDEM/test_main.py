import unittest

from main import calculate_coordinates


class TestCalculateCoordinates(unittest.TestCase):
    def test_North_East(self):
        lat, long = calculate_coordinates(38.59, 4.5)
        self.assertEqual(lat, 38)
        self.assertEqual(long, 4)

    def test_North_Western(self):
        lat, long = calculate_coordinates(38.359, -5.9)
        self.assertEqual(lat, 38)
        self.assertEqual(long, -6)

    def test_South_East(self):
        lat, long = calculate_coordinates(-38.69, 4.96)
        self.assertEqual(lat, -39)
        self.assertEqual(long, 4)

    def test_South_Western(self):
        lat, long = calculate_coordinates(-38.69, -4.96)
        self.assertEqual(lat, -39)
        self.assertEqual(long, -5)


if __name__ == "__main__":
    unittest.main()
