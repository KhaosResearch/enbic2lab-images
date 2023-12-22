import shutil
import unittest
from pathlib import Path
import os

from main import main 


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        self.test_filepath = "test_dataset.csv"
        self.test_filepath_predictions = "test_predictions.csv"
        self.test_output_path = "test_output"

    def tearDown(self):
        # Clean up after the test
        os.remove(self.test_filepath)
        os.remove(self.test_filepath_predictions)
        
        # Use shutil.rmtree to remove the directory and its contents
        shutil.rmtree(self.test_output_path, ignore_errors=True)

    def test_main_generates_png(self):
        # Create some dummy data
        # You may want to modify this depending on the structure of your actual data
        dummy_data = """date;pollen
        1992-02-01;0.0
1992-03-01;180.57480000000004
1992-04-01;16.660175000000002
1992-05-01;1.07485
        """

        # Write dummy data to files
        with open(self.test_filepath, "w") as file:
            file.write(dummy_data)

        dummy_predictions = "10;15;20"
        with open(self.test_filepath_predictions, "w") as file:
            file.write(dummy_predictions)

        # Create the output directory
        os.makedirs(self.test_output_path, exist_ok=True)

        # Call the main function
        main(
            self.test_filepath,
            self.test_filepath_predictions,
            self.test_output_path,
            validation_time="1990-01-01",
            delimiter=";",
        )

        # Check if the PNG file is generated
        expected_png_path = Path(self.test_output_path, "Sarima_visualisation.png")
        self.assertTrue(expected_png_path.exists(), "PNG file not generated.")


if __name__ == "__main__":
    unittest.main()
