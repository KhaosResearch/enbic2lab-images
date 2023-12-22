import unittest
from main import main  # Import the main function from your script file
import os


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # Create a temporary input CSV file with sample data
        self.filepath = "sample_file.csv"
        with open(self.filepath, "w") as file:
            file.write("Fecha,Precipitación\n")
            file.write("01/01/2023,1.0\n")
            file.write("02/01/2023,2.0\n")
            file.write("03/01/2023,20.0\n")
            file.write("04/01/2023,0.0\n")
            file.write("05/01/2023,12.0\n")
            file.write("06/01/2023,5.0\n")
            file.write("07/01/2023,4.0\n")

        self.delimiter = ","
        self.output_filepath = "output.html"

    def tearDown(self):
        # Remove the temporary input CSV file after the test
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        # Remove the output HTML file if it was created during the test
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def test_main_function(self):
        # Call the main function
        main(self.filepath, self.output_filepath, self.delimiter)

        # Assertions
        self.assertTrue(
            os.path.exists(self.output_filepath)
        )  # Check if the output file was created


if __name__ == "__main__":
    unittest.main()
