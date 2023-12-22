import os
import tempfile
import unittest
import pandas as pd
from io import StringIO
from main import scale_by_months

SAMPLE_CSV_DATA = """fecha;value1;value2
2023-01-01;1;2
2023-01-05;3;4
2023-02-10;5;6
2023-02-15;7;8"""

class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_file = os.path.join(self.temp_dir.name, "test_data.csv")
        with open(self.temp_csv_file, "w") as f:
            f.write(SAMPLE_CSV_DATA)

    def test_scale_by_months(self):
        # Llama a la función con el archivo CSV temporal y verifica el resultado
        output = os.path.join(self.temp_dir.name, "output_data.csv")
        scale_by_months(self.temp_csv_file, ';', 'fecha', output)

        # Verifica que el archivo de salida se haya creado y cerrado correctamente
        with open(output, "r") as f:
            content = f.read()
            self.assertTrue(content)  # Verifica que el archivo no está vacío

        # Lee el archivo de salida generado por la función
        df = pd.read_csv(output, sep=';')

        # Verifica que la suma de los valores por mes sea correcta
        expected_output = """fecha;value1;value2
                            2023-01;4;6
                            2023-02;12;14"""
        expected_df = pd.read_csv(StringIO(expected_output), sep=';')

        # Compara los DataFrames
        expected_df['fecha'] = expected_df['fecha'].str.strip()
        pd.testing.assert_frame_equal(df, expected_df)

    def tearDown(self):
        # Elimina el archivo CSV temporal después de las pruebas
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
