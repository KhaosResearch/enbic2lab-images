import unittest
import pandas as pd
import tempfile
import numpy as np
from main import test_stationary, find_best_arima_model, decompose_and_analyze,arima_analysis
import shutil
import os


class TestFunctions(unittest.TestCase):
    def setUp(self):
        # Genera una serie de tiempo con 120 filas (10 años) con estacionalidad mensual
        dates = pd.date_range(start='2013-01-01', periods=120, freq='M')
        formatted_dates = dates.strftime('%Y-%m-%d')
        # Crea una componente estacional con una frecuencia de 12 meses
        seasonal_component = np.sin(2 * np.pi * np.arange(120) / 12)
        # Crea una serie temporal estacionaria con una tendencia lineal y la componente estacional
        pollen_values = np.linspace(1, 10, 120) + seasonal_component
        self.data = pd.DataFrame({'polen': pollen_values, 'fecha':formatted_dates}) #'fecha': dates,
        self.data = self.data.set_index('fecha')

        print(self.data)
        self.output_path = tempfile.mkdtemp() + '/'
        print(self.output_path)

    def teardown(self):
        # Elimina el directorio temporal y su contenido después de que las pruebas se ejecuten
        shutil.rmtree(self.output_path)

    def test_test_stationary(self):
        df = test_stationary(self.data, self.output_path)
        self.assertTrue("Test statistic" in df.index)
        self.assertTrue("p-value" in df.index)
        self.assertTrue("Confidence 90 %" in df.index)
        self.assertTrue("Confidence 95 %" in df.index)
        self.assertTrue("Confidence 99 %" in df.index)

    def test_decompose_and_analyze(self):
        dickey_fuller = pd.DataFrame(index=["Test statistic", "p-value", "Confidence 90 %", "Confidence 95 %", "Confidence 99 %"])
        decompose_and_analyze(self.data['polen'], 2015, dickey_fuller, self.output_path)
        arima_analysis(self.data['polen'], self.output_path)
        # Nos aseguramos que los archivos esperados se hayan creado en el directorio de salida
        self.assertTrue(os.path.exists(self.output_path + "seasonality.pdf"))
        self.assertTrue(os.path.exists(self.output_path + "DickerFuller_seasonality.csv"))
        self.assertTrue(os.path.exists(self.output_path + "SARIMAX_plots.pdf"))

if __name__ == "__main__":
    unittest.main()

