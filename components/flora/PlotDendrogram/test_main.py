import os
import tempfile
import unittest

from main import main


class PlotDendrogramTestCase(unittest.TestCase):
    def test_main(self):
        # Test case 1: Test with a small CSV file

        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
            # Write data to the CSV file
            temp_csv.write(
                b";A;B;C;D;E\n"
                b"U-P1;0.0;0.1;0.2;0.0;0.0\n"
                b"U-P2;0.3;0.0;0.0;0.0;1.1\n"
                b"U-P3;0.0;0.2;0.0;3.0;0.0\n"
                b"U-P4;0.4;0.0;0.0;0.0;1.0\n"
                b"U-P5;0.0;0.0;0.4;0.0;0.0"
            )
            temp_csv.seek(0)

            # Create a temporary output file
            with tempfile.NamedTemporaryFile(
                suffix=".png", delete=False
            ) as temp_output:
                output = temp_output.name

                # Call the main function with the file paths and parameters
                main(temp_csv.name, ",", "euclidean", "ward", "top", output)

                # Assert that the output file was created
                assert os.path.isfile(output)


if __name__ == "__main__":
    unittest.main()
