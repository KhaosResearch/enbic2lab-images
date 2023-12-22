import os
import tempfile
import unittest

import pandas as pd

from main import clean_data_frame, main


class CleanDataFrameTestCase(unittest.TestCase):
    def test_clean_data_frame(self):
        # Test case 1: Clean element with "-"
        self.assertEqual(clean_data_frame("-"), 0)

        # Test case 2: Clean element with "x"
        self.assertEqual(clean_data_frame("x"), 0)

        # Test case 3: Clean element with "X"
        self.assertEqual(clean_data_frame("X"), 0)

        # Test case 4: Clean element with "."
        self.assertEqual(clean_data_frame("."), 0)

        # Test case 5: Clean element with "+"
        self.assertEqual(clean_data_frame("+"), 0.2)

        # Test case 6: Clean element with "+.2"
        self.assertEqual(clean_data_frame("+.2"), 0.2)

        # Test case 7: Clean element with "(+)"
        self.assertEqual(clean_data_frame("(+)"), 0.1)

        # Test case 8: Clean element not in the mapping
        self.assertEqual(clean_data_frame("123"), 123)


class TestMain(unittest.TestCase):
    def test_main(self):
        # Test case 1: CSV file with default delimiter
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
            # Create a temporary CSV file with sample data
            temp_csv.write(
                b"Plot orientation,1,4,7\nPlot slope,2,5,8\nAlt. Veg. (cm),3,6,9\nSpecies,S1,S2,S3\nS1,1,-,0.4\nS2,+,5,1\nS3,1,4,(+)"
            )
            temp_csv.seek(0)

            with tempfile.NamedTemporaryFile(
                suffix=".csv", delete=False
            ) as temp_output:
                output = temp_output.name
                # Call the main function with the temporary CSV file, default delimiter (","), and output file
                main(temp_csv.name, ",", output)
                self.assertTrue(os.path.exists(output))

                # Read the output file as a DataFrame
                df_output = pd.read_csv(output, sep=",")
                # Define the expected output DataFrame
                expected_output = pd.DataFrame(
                    {
                        "Unnamed: 0": [1, 4, 7],
                        "S1": [1, 0, 0.4],
                        "S2": [0.2, 5, 1],
                        "S3": [1, 4, 0.1],
                    }
                )
                # Assert that the output DataFrame matches the expected output
                pd.testing.assert_frame_equal(df_output, expected_output)

        # Test case 2: CSV file with tab delimiter
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
            # Create a temporary CSV file with sample data
            temp_csv.write(
                b"Plot orientation\t1\t4\t7\nPlot slope\t2\t5\t8\nAlt. Veg. (cm)\t3\t6\t9\nSpecies\tS1\tS2\tS3\nS1\t1\t-\t0.4\nS2\t+\t5\t1\nS3\t1\t4\t(+)"
            )
            temp_csv.seek(0)

            with tempfile.NamedTemporaryFile(
                suffix=".csv", delete=False
            ) as temp_output:
                output = temp_output.name
                # Call the main function with the temporary CSV file, tab delimiter ("\t"), and output file
                main(temp_csv.name, "\t", output)
                self.assertTrue(os.path.exists(output))

                # Read the output file as a DataFrame
                df_output = pd.read_csv(output, sep="\t")
                # Define the expected output DataFrame
                expected_output = pd.DataFrame(
                    {
                        "Unnamed: 0": [1, 4, 7],
                        "S1": [1, 0, 0.4],
                        "S2": [0.2, 5, 1],
                        "S3": [1, 4, 0.1],
                    }
                )
                # Assert that the output DataFrame matches the expected output
                pd.testing.assert_frame_equal(df_output, expected_output)


if __name__ == "__main__":
    unittest.main()
