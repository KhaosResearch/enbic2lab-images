import os
import tempfile
import unittest

from main import main


class CSV2HTMLTestCase(unittest.TestCase):
    def test_main(self):
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv:
            # Write data to the CSV file
            temp_csv.write(
                b"A;B;C\n"
                b"1;1;4\n"
                b"2;3;5\n"
                b"3;5;1\n"
                b"4;2;3"
            )
            temp_csv.seek(0)

            # Create a temporary output file
            with tempfile.NamedTemporaryFile(
                suffix=".html", delete=False
            ) as temp_output:
                output = temp_output.name

                # Call the main function with the file paths and parameters
                main(temp_csv.name, ";", output)

                # Assert that the output file was created
                assert os.path.isfile(output)


if __name__ == "__main__":
    unittest.main()
