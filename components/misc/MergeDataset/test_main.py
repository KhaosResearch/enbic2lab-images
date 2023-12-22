import unittest
import pandas as pd
import os
from io import StringIO
from main import main

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        input_data1 = """col1;col2
A;1
B;2
C;3"""

        input_data2 = """col1;col2
X;4
Y;5
Z;6"""

        self.filepath1 = "mnt/shared/test_file1.csv"
        self.filepath2 = "mnt/shared/test_file2.csv"
        self.output_path = "mnt/shared/test_output.csv"

        with open(self.filepath1, "w") as f:
            f.write(input_data1)

        with open(self.filepath2, "w") as f:
            f.write(input_data2)

    def tearDown(self):
        # Delete the test files after the test is complete
        os.remove(self.filepath1)
        os.remove(self.filepath2)
        os.remove(self.output_path)

    def test_main(self):
        # Run the main function with sample data
        main(self.filepath1, self.filepath2, self.output_path, delimiter1=";", delimiter2=";")

        # Read the output CSV for assertions
        output_df = pd.read_csv(self.output_path, delimiter=";")

        # Define the expected output
        expected_output = """col1;col2
A;1
B;2
C;3
X;4
Y;5
Z;6"""

        expected_df = pd.read_csv(StringIO(expected_output), delimiter=";")

        # Check if the output matches the expected result
        pd.testing.assert_frame_equal(output_df, expected_df)

if __name__ == '__main__':
    unittest.main()