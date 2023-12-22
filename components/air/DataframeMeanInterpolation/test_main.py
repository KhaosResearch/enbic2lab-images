import os
import unittest
import pandas as pd
from io import StringIO
from main import main  # Replace 'your_script_name' with the actual name of your script

class TestFillMissingData(unittest.TestCase):
    def setUp(self):

        # Create a sample CSV file
        sample_data = """fecha;tmed;tmin;tmax;dir;velmedia;racha;sol;presMax;presMin;Platanus;DOY;prec
1991-05-11;;;;;;;;;;;;
1994-05-11;18.3;13.4;23.2;32.0;4.4;12.5;7.5;1012.3;1009.6;0.0;131;1.0
1994-05-12;15.9;9.2;22.6;24.0;4.7;8.9;11.5;1011.1;1005.0;0.0;132;0.0
1994-05-13;16.1;13.0;19.2;26.0;4.2;11.4;5.2;1010.6;1004.1;0.0;133;4.3
1994-05-14;14.7;9.0;20.4;18.0;3.9;8.9;9.2;1012.6;1009.6;0.0;134;0.0
1995-05-11;22.4;18.4;26.4;32.0;6.9;13.6;9.6;1010.2;1006.7;0.0;131;0.0
1995-05-12;;15.0;25.6;32.0;7.2;16.4;12.8;1013.8;1009.9;0.0;132;0.0
1995-05-13;20.5;15.6;25.4;30.0;3.6;10.3;12.3;1015.8;1013.5;0.0;133;0.0
1995-05-14;16.8;12.0;21.6;14.0;2.5;6.7;11.5;1017.6;1015.4;0.0;134;0.0
"""
        self.filepath = "test_file1.csv"
        self.output_path = "test_output.csv"
        with open(self.filepath, "w") as f:
            f.write(sample_data)


    def tearDown(self):
        # Delete the test files after the test is complete
        os.remove(self.filepath)
        os.remove(self.output_path)
        
    def test_fill_missing_data(self):

        # Test
        main(self.filepath, self.output_path, '1991', '1996', "fecha", ";")
        result_df = pd.read_csv(self.output_path, delimiter=';', parse_dates=['fecha'], dayfirst=True)

        # Assert
        self.assertEqual(result_df["tmed"][0], 20.35)
        self.assertEqual(result_df["prec"][0], 0.5)


if __name__ == "__main__":
    unittest.main()