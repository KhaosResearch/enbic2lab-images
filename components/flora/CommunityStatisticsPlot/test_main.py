import os
import tempfile
import unittest

from main import plot_data, read_csv

SAMPLE_CSV_DATA = """Community;Min_Alt;Max_Alt
Community A;100;200
Community B;150;250
Community C;200;300
"""


class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_file = os.path.join(self.temp_dir.name, "sample.csv")
        with open(self.temp_csv_file, "w") as f:
            f.write(SAMPLE_CSV_DATA)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_read_csv(self):
        labels, min_altitude, max_altitude = read_csv(self.temp_csv_file, ";")
        self.assertEqual(len(labels), 3)
        self.assertEqual(len(min_altitude), 3)
        self.assertEqual(len(max_altitude), 3)
        self.assertEqual(labels, ["Community A", "Community B", "Community C"])
        self.assertEqual(min_altitude, [100.0, 150.0, 200.0])
        self.assertEqual(max_altitude, [200.0, 250.0, 300.0])

    def test_read_csv_file_not_found(self):
        labels, min_altitude, max_altitude = read_csv("nonexistent.csv", ";")
        self.assertEqual(labels, [])
        self.assertEqual(min_altitude, [])
        self.assertEqual(max_altitude, [])

    def test_read_csv_invalid_column_name(self):
        with open(self.temp_csv_file, "w") as f:
            f.write("InvalidColumn;400;500\n")

        labels, min_altitude, max_altitude = read_csv(self.temp_csv_file, ";")
        self.assertEqual(labels, [])
        self.assertEqual(min_altitude, [])
        self.assertEqual(max_altitude, [])

    def test_plot_data(self):
        labels = ["Community A", "Community B", "Community C"]
        min_altitude = [100.0, 150.0, 200.0]
        max_altitude = [200.0, 250.0, 300.0]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "output.pdf")
            plot_data(labels, min_altitude, max_altitude, temp_output_file)
            self.assertTrue(os.path.exists(temp_output_file))


if __name__ == "__main__":
    unittest.main()
