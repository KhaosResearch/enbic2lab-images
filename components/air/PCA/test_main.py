import unittest
import pandas as pd
import tempfile
import os
import numpy as np
from main import pca_analysis


class TestPCAAnalysis(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        num_samples = 1000
        num_features = 10
        random_data = np.random.rand(num_samples, num_features)
        date_range = pd.date_range(start='2022-01-01', periods=num_samples)
        self.temp_csv_file = os.path.join(self.temp_dir.name, "test_data.csv")
        data = {
            "date": date_range,
            "pollen": np.random.randint(0, 2, num_samples),  # Datos sintéticos para la columna "pollen"
        }
        for i in range(num_features):
            data[f"Feature_{i + 1}"] = random_data[:, i]
        pd.DataFrame(data).to_csv(self.temp_csv_file, index=False)

    def test_pca_analysis(self):
        # Perform PCA analysis using the temporary CSV file in test mode
        output_path = os.path.join(self.temp_dir.name, "result_pca.csv")

        # Perform PCA analysis
        pca_analysis(self.temp_csv_file, ",", "pollen", "date", output_path, 0.7)

        # Verificar si el archivo de salida del PCA se ha generado en el directorio temporal
        self.assertTrue(os.path.exists(output_path))

        pca_dataframe = pd.read_csv(output_path, sep=',')

        # Check if the number of columns after PCA is within the expected range
        self.assertLessEqual(pca_dataframe.shape[1], 11)  # 10 PCs + pollen_type

    def tear_down(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
