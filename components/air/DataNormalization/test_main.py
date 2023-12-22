import os
import unittest
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import tempfile
from pathlib import Path
from main import minmax_scaler, data_normalization

class TestNormalizationFunctions(unittest.TestCase):
    def setUp(self):
        # Crear un archivo CSV temporal con datos de prueba
        self.output_path = tempfile.TemporaryDirectory()
        self.sample_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'pollen': [1, 2, 3],
            'feature1': [4, 5, 6],
            'feature2': [7, 8, 9]
        })
        # self.output_path = Path('output')

    def test_minmax_scaler(self):
        data = self.sample_data[['feature1', 'feature2']]
        scaled_data, scaler = minmax_scaler(data)

        # Verificar que los datos escalados están en el rango [0, 1]
        self.assertTrue(np.all(scaled_data >= 0) and np.all(scaled_data <= 1))

        # Verificar que el scaler es una instancia de MinMaxScaler
        self.assertIsInstance(scaler, MinMaxScaler)

    def test_data_normalization(self):

        # Crear un archivo temporal con los datos de ejemplo

        sample_file = os.path.join(self.output_path.name, "sample_data.csv")
        self.sample_data.to_csv(sample_file, index=False)

        # print(self.sample_data)

        # Llamar a la función de normalización
        data_normalization(sample_file, ',', 'pollen', 'date', self.output_path.name)

        # Verificar que los archivos de salida existen
        features_file = os.path.join(self.output_path.name,'features.csv')
        target_file = os.path.join(self.output_path.name,'target.csv')
        scaler_features_file = os.path.join(self.output_path.name, 'scaler_features.pkl')
        scaler_target_file = os.path.join(self.output_path.name, 'scaler_target.pkl')

        self.assertTrue(Path(features_file).exists())
        self.assertTrue(Path(target_file).exists())
        self.assertTrue(Path(scaler_features_file).exists())
        self.assertTrue(Path(scaler_target_file).exists())

        # Verificar que los datos en los archivos coinciden con los datos escalados
        scaled_features = np.loadtxt(features_file, delimiter=',')
        scaled_target = np.loadtxt(target_file, delimiter=',')

        self.assertTrue((scaled_features >= 0).all().all() and (scaled_features <= 1).all().all())
        self.assertTrue((scaled_target >= 0).all().all() and (scaled_target <= 1).all().all())

        # Verificar que los scalers pueden cargarse correctamente
        loaded_scaler_features = joblib.load(str(scaler_features_file))
        loaded_scaler_target = joblib.load(str(scaler_target_file))

        self.assertIsInstance(loaded_scaler_features, MinMaxScaler)
        self.assertIsInstance(loaded_scaler_target, MinMaxScaler)


    def tearDown(self):
        self.output_path.cleanup()


if __name__ == '__main__':
    unittest.main()


