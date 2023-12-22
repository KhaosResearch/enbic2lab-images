import unittest
import pandas as pd
import tempfile
import os
from main import lagged_time_series

class TestLaggedTimeSeries(unittest.TestCase):
    def setUp(self):
        # Crear un archivo CSV temporal con datos de prueba
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_file = os.path.join(self.temp_dir.name, "test_data.csv")
        data = {
            'date_column': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'pollen_column': [1, 2, 3, 4, 5],
            'feature1': [10, 20, 30, 40, 50],
            'feature2': [15, 25, 35, 45, 55]
        }
        self.test_dataframe = pd.DataFrame(data)
        self.test_dataframe.to_csv(self.temp_csv_file, sep=';', index=False)

    def test_lagged_time_series(self):
        lags = 2
        output_file = os.path.join(self.temp_dir.name, "output_data.csv")
        lagged_time_series(self.temp_csv_file, ';', 'date_column', lags, 'pollen_column', output_file)

        # Leer el archivo de salida
        output_dataframe = pd.read_csv(output_file, sep=';')

        # Verificar que las columnas lagged se han creado correctamente
        expected_columns = ['date_column','pollen_column','feature1', 'feature2', 'feature1 (t-1)', 'feature2 (t-1)', 'feature1 (t-2)', 'feature2 (t-2)']
        self.assertEqual(list(output_dataframe.columns), expected_columns)

        # Verificar que los valores lagged son correctos
        self.assertEqual(output_dataframe.at[2, 'feature1 (t-1)'], 40)  # El valor de feature1 en t-1 es 40
        self.assertEqual(output_dataframe.at[2, 'feature2 (t-2)'], 35)  # El valor de feature2 en t-2 es 35

    def tearDown(self):
        # Eliminar el directorio temporal después de las pruebas
        self.temp_dir.cleanup()

if __name__ == "__main__":
    unittest.main()

