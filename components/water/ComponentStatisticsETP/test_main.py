import unittest
import os
import pandas as pd
import numpy as np
from main import main
from scipy import stats


class TestETPStatistics(unittest.TestCase):
    def tearDown(self):
        files_to_delete = ["test_input.csv", "ETP_StatisticsPrueba.csv"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    def test_metrics_calculation(self):
        # Define test parameters
        delimiter = ";"
        start_year = 2000
        end_year = 2005
        variables_list = "TMAX TMIN"
        metrics_list = "Mean Median Min Max Range Variance Standard-Deviation Variation-Coefficient Asymmetry-Coefficient Kurtosis"
        hydrological_year = False
        output_filepath = "ETP_StatisticsPrueba.csv"

        # Create a sample input CSV file
        input_data = """Fecha;TMAX;TMIN
01/10/2003;20.988;16.505
02/10/2003;19.495;15.677
"""
        with open("test_input.csv", "w") as f:
            f.write(input_data)

        # Run the main function
        main(
            "test_input.csv",
            output_filepath,
            start_year,
            end_year,
            variables_list,
            metrics_list,
            hydrological_year,
            delimiter,
        )

        # Perform assertions on the output file
        result_df = pd.read_csv(
            output_filepath,
            delimiter=delimiter,
            index_col=0,
            header=None,
            names=["Metric"],
        )

        # Add assertions based on expected output for each metric
        expected_values = {
            "TMAX_Mean": np.mean([20.988, 19.495]),
            "TMAX_Median": np.median([20.988, 19.495]),
            "TMAX_Min": np.min([20.988, 19.495]),
            "TMAX_Max": np.max([20.988, 19.495]),
            "TMAX_Range": np.max([20.988, 19.495]) - np.min([20.988, 19.495]),
            "TMAX_Variance": np.var([20.988, 19.495]),
            "TMAX_Standard-Deviation": np.std([20.988, 19.495]),
            "TMAX_Variation-Coefficient": stats.variation([20.988, 19.495]),
            "TMAX_Asymmetry-Coefficient": stats.skew(
                [20.988, 19.495], axis=0, bias=True
            ),
            "TMAX_Kurtosis": stats.kurtosis(
                [20.988, 19.495], axis=0, fisher=True, bias=True
            ),
            "TMIN_Mean": np.mean([16.505, 15.677]),
            "TMIN_Median": np.median([16.505, 15.677]),
            "TMIN_Min": np.min([16.505, 15.677]),
            "TMIN_Max": np.max([16.505, 15.677]),
            "TMIN_Range": np.max([16.505, 15.677]) - np.min([16.505, 15.677]),
            "TMIN_Variance": np.var([16.505, 15.677]),
            "TMIN_Standard-Deviation": np.std([16.505, 15.677]),
            "TMIN_Variation-Coefficient": stats.variation([16.505, 15.677]),
            "TMIN_Asymmetry-Coefficient": stats.skew(
                [16.505, 15.677], axis=0, bias=True
            ),
            "TMIN_Kurtosis": stats.kurtosis(
                [16.505, 15.677], axis=0, fisher=True, bias=True
            ),
        }

        for metric, expected_value in expected_values.items():
            print(metric)
            self.assertEqual(
                round(result_df.loc[metric, "Metric"], 3), round(expected_value, 3)
            )


if __name__ == "__main__":
    unittest.main()
