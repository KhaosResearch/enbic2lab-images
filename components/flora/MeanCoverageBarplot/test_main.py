import os
import tempfile
import unittest

from main import main


class MeanCoverageBarPlotTestCase(unittest.TestCase):
    def test_main(self):
        # Test case 1: Test with a small CSV file

        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
            # Write data to the CSV file
            temp_csv.write(
                b"Community;Mean Coverage;Mean Coverage Standard Error\n"
                b"S1;1;4\n"
                b"S2;3;5\n"
                b"S3;5;1\n"
                b"S4;2;3"
            )
            temp_csv.seek(0)

            # Create a temporary output file
            with tempfile.NamedTemporaryFile(
                suffix=".pdf", delete=False
            ) as temp_output:
                output = temp_output.name

                # Call the main function with the file paths and parameters
                main(temp_csv.name, ";", 3, "#006400", output)

                # Assert that the output file was created
                assert os.path.isfile(output)


if __name__ == "__main__":
    unittest.main()
