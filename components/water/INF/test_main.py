import unittest
import pandas as pd
from main import main
import os


class TestINFCalculator(unittest.TestCase):
    def tearDown(self):
        files_to_delete = ["test_input.csv", "output_test.csv"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    def test_inf_calculation(self):
        delimiter = ";"
        p_zero = "4"
        output_filepath = "output_test.csv"
        input_data = """LLU
0
21
58
4
10
        """
        with open("test_input.csv", "w") as f:
            f.write(input_data)

        main("test_input.csv", output_filepath, delimiter, p_zero)

        result_df = pd.read_csv(output_filepath, delimiter=delimiter)
        print(result_df["INF"])
        expected_output = [0, round(13.189, 2), round(18.594, 2), 4, round(8.615, 2)]

        for i in range(len(result_df)):
            self.assertEqual(round(result_df.loc[i, "INF"], 2), expected_output[i])


if __name__ == "__main__":
    unittest.main()
