import unittest
import pandas as pd
from io import StringIO
from main import main 
import os

class TestScriptFunctionality(unittest.TestCase):

    def test_main(self):
        # Sample data for testing
        input_data = """filename;r2_mean;mae_mean;rmse_mean;rmse_mae_mean
test_mean;0.9;1.5;2.0;2
test_pandas;0.85;1.7;2.2;1.9"""
        with open("mnt/shared/test_metrics.csv", "w") as f:
            f.write(input_data)
        
        mean_data = """col1;col2
A;10
B;20
C;30"""
        with open("mnt/shared/test_mean.csv", "w") as f:
            f.write(mean_data)

        pandas_data = """col1;col2
X;15
Y;25
Z;35"""
        with open("mnt/shared/test_pandas.csv", "w") as f:
            f.write(pandas_data)

        

        # Specify the output path for the test
        output_path = "mnt/shared/test_output.csv"

        # Run the main function with sample data
        main("mnt/shared/test_metrics.csv", "mnt/shared/test_pandas.csv", "mnt/shared/test_mean.csv", output_path)

        # Read the output CSV for assertions
        output_df = pd.read_csv(output_path,delimiter=";")

        self.assertEqual(output_df["col1"][0], "A")  
    def tearDown(self):
        # Delete the test files after the test is complete
        os.remove("mnt/shared/test_metrics.csv")
        os.remove("mnt/shared/test_mean.csv")
        os.remove("mnt/shared/test_pandas.csv")
        os.remove("mnt/shared/test_output.csv")
if __name__ == '__main__':
    unittest.main()
