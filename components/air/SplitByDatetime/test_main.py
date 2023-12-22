import unittest
import pandas as pd
import tempfile
import os
from main import split_by_datetime

class TestSplitByDatetime(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_csv_file = os.path.join(self.temp_dir.name, "synthetic.csv")
        data = {
            'fecha': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01','2023-05-01'],
            'value': [1, 2, 3, 4, 5]
        }
        self.test_dataframe = pd.DataFrame(data)
        self.test_dataframe.to_csv(self.temp_csv_file, index=False, sep=';')

    def test_split_by_datetime(self):
        start_date = '2023-02-01'
        end_date = '2023-04-01'
        output_file = os.path.join(self.temp_dir.name, "output_data.csv")
        split_by_datetime(self.temp_csv_file, ';', 'fecha', start_date, end_date, output_file)

        # Leer el archivo de salida
        output_dataframe = pd.read_csv(output_file, sep=';')

        # Verificar que las fechas estén dentro del rango esperado
        dates = pd.to_datetime(output_dataframe['fecha'])
        for date in dates:
            self.assertGreaterEqual(date, pd.to_datetime(start_date))
            self.assertLessEqual(date, pd.to_datetime(end_date))

    def tearDown(self):
        # Eliminar el directorio temporal después de las pruebas
        self.temp_dir.cleanup()

if __name__ == "__main__":
    unittest.main()
