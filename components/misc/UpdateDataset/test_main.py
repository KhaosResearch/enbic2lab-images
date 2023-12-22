import unittest
import pandas as pd
import os
from io import StringIO
from main import main

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        input_data1 = """fecha;tmed;prec;tmin;tmax;dir;velmedia;racha;sol;presMax;presMin;Platanus;DOY
1991-05-11;17.3;;11.6;23.0;30.0;3.6;9.2;9.0;1019.4;1015.1;;131
1991-05-12;15.3;0.0;11.0;19.6;14.0;3.6;7.8;12.0;1023.4;1019.4;;132
1991-05-13;16.7;0.0;10.2;23.2;17.0;5.0;10.8;12.2;1023.4;1020.9;;133
1991-05-14;16.1;0.0;10.2;22.0;14.0;3.3;7.8;12.1;1023.4;1020.3;;134
1991-05-15;16.6;0.0;10.2;23.0;14.0;3.3;8.3;12.3;1021.1;1016.6;;135
1991-05-16;22.1;0.0;13.0;31.2;14.0;2.5;8.3;12.4;1017.6;1014.4;;136
1991-05-17;18.8;0.0;16.0;21.6;14.0;2.8;8.3;10.9;1019.1;1017.4;;137
1991-05-18;18.6;0.0;15.8;21.4;17.0;2.8;7.8;11.2;1020.1;1017.1;;138
1991-05-19;19.1;0.0;17.2;21.0;14.0;3.1;6.7;12.0;1020.5;1018.2;;139
1991-05-20;18.3;0.0;14.4;22.2;14.0;2.8;7.2;12.1;1023.8;1020.1;;140
1991-05-21;17.1;0.0;12.2;22.0;12.0;3.6;5.8;11.3;1029.6;1023.3;;141
1991-05-22;17.6;0.0;14.6;20.6;12.0;4.4;10.0;12.2;1030.3;1026.7;;142"""

        input_data2 = """DATE;6155A
1991-05-11;0.3
1991-05-12;0.4
1991-05-13;0.0
1991-05-14;0.0
1991-05-15;0.0
1991-05-16;0.0
1991-05-17;0.0
1991-05-18;0.0
1991-05-19;0.0
1991-05-20;0.0
1991-05-21;0.0
1991-05-22;0.0"""

        self.filepath1 = "test_file1.csv"
        self.filepath2 = "test_file2.csv"
        self.output_path = "test_output.csv"

        with open(self.filepath1, "w") as f:
            f.write(input_data1)

        with open(self.filepath2, "w") as f:
            f.write(input_data2)

    def tearDown(self):
        # Delete the test files after the test is complete
        os.remove(self.filepath1)
        os.remove(self.filepath2)
        os.remove(self.output_path)

    def test_main(self):
        # Run the main function with sample data
        main(self.filepath1, self.filepath2,"fecha", "DATE", self.output_path, 'prec', '6155A',  ";", ";")

        # Read the output CSV for assertions
        output_df = pd.read_csv(self.output_path, delimiter=";")

        # Define the expected output
        expected_output = """fecha;tmed;tmin;tmax;dir;velmedia;racha;sol;presMax;presMin;Platanus;DOY;prec
1991-05-11;17.3;11.6;23.0;30.0;3.6;9.2;9.0;1019.4;1015.1;;131;0.3
1991-05-12;15.3;11.0;19.6;14.0;3.6;7.8;12.0;1023.4;1019.4;;132;0.4
1991-05-13;16.7;10.2;23.2;17.0;5.0;10.8;12.2;1023.4;1020.9;;133;0.0
1991-05-14;16.1;10.2;22.0;14.0;3.3;7.8;12.1;1023.4;1020.3;;134;0.0
1991-05-15;16.6;10.2;23.0;14.0;3.3;8.3;12.3;1021.1;1016.6;;135;0.0
1991-05-16;22.1;13.0;31.2;14.0;2.5;8.3;12.4;1017.6;1014.4;;136;0.0
1991-05-17;18.8;16.0;21.6;14.0;2.8;8.3;10.9;1019.1;1017.4;;137;0.0
1991-05-18;18.6;15.8;21.4;17.0;2.8;7.8;11.2;1020.1;1017.1;;138;0.0
1991-05-19;19.1;17.2;21.0;14.0;3.1;6.7;12.0;1020.5;1018.2;;139;0.0
1991-05-20;18.3;14.4;22.2;14.0;2.8;7.2;12.1;1023.8;1020.1;;140;0.0
1991-05-21;17.1;12.2;22.0;12.0;3.6;5.8;11.3;1029.6;1023.3;;141;0.0
1991-05-22;17.6;14.6;20.6;12.0;4.4;10.0;12.2;1030.3;1026.7;;142;0.0"""

        expected_df = pd.read_csv(StringIO(expected_output), delimiter=";")

        # Check if the output matches the expected result
        pd.testing.assert_frame_equal(output_df, expected_df)

if __name__ == '__main__':
    unittest.main()