import unittest
import pandas as pd
from main import main
import os


class TestLLUCalculator(unittest.TestCase):
    def tearDown(self):
        files_to_delete = ["test_input.csv", "output_test.csv"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    def test_llu_calculation(self):
        # Datos de entrada para las pruebas
        delimiter = ";"
        ru = "50"
        etp_name = "Hargreaves"
        output_filepath = "output_test.csv"
        input_data = """ETP Hargreaves;Precipitación
2;20
10;30
2;45
10;60
2;5
1;53
        """
        with open("test_input.csv", "w") as f:
            f.write(input_data)

        main("test_input.csv", output_filepath, delimiter, ru, etp_name)

        result_df = pd.read_csv(output_filepath, delimiter=delimiter)

        print(result_df)

        expected_output = [0, 0, 0, 21, 58, 4]

        for i in range(len(result_df)):
            self.assertEqual(result_df.loc[i, "LLU"], expected_output[i])


if __name__ == "__main__":
    unittest.main()
