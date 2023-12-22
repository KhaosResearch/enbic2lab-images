import os
import tempfile
import unittest

import pandas as pd

from main import main


class InventoryStatisticsTestCase(unittest.TestCase):
    def test_main(self):
        # Create a temporary directory to store the test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary input CSV file
            input_file = os.path.join(temp_dir, "input.csv")
            with open(input_file, "w") as f:
                f.write("Plot orientation,1,4,7\n")
                f.write("Plot slope,2,5,8\n")
                f.write("Alt. Veg. (cm),3,6,9")

            # Create a temporary output CSV file
            output_file = os.path.join(temp_dir, "output.csv")

            # Run the main function with the test input and output files
            main(input_file, ",", output_file)

            # Read the output CSV file into a DataFrame
            df_output = pd.read_csv(output_file, sep=",")

            # Define the expected mean values
            mean_orientation = (1 + 4 + 7) / 3
            mean_slope = (2 + 5 + 8) / 3
            mean_alt_veg = (3 + 6 + 9) / 3

            # Check if the mean values are correct
            assert df_output.loc[0, "Mean Orientation"] == mean_orientation
            assert df_output.loc[0, "Mean Slope"] == mean_slope
            assert df_output.loc[0, "Mean Alt. Veg. (cm)"] == mean_alt_veg


if __name__ == "__main__":
    unittest.main()
