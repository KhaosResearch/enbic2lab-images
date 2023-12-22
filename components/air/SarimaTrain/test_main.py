import unittest
import pandas as pd
from pathlib import Path
from main import optimizeSARIMA, parameter_configuration

class TestSARIMA(unittest.TestCase):

    def setUp(self):
        # Create a simple DataFrame for testing
        data = {
            'date': ['1992-02', '1992-03', '1992-04', '1992-05'],
            'pollen': [0.0, 0.0, 0.0, 0.0],
            'other_column': [1, 2, 3, 4]
        }
        self.df = pd.DataFrame(data)

    def test_parameter_configuration(self):
        parameters = parameter_configuration()
        self.assertIsInstance(parameters, list)
        self.assertTrue(all(isinstance(param, tuple) and len(param) == 6 for param in parameters))

    def test_optimizeSARIMA(self):
        s = 12  # Assuming seasonality is 12 for testing
        parameters_list = parameter_configuration()
        result_table = optimizeSARIMA(self.df, parameters_list, s)

        self.assertIsInstance(result_table, pd.DataFrame)
        self.assertTrue('parameters' in result_table.columns)
        self.assertTrue('aic' in result_table.columns)

if __name__ == '__main__':
    unittest.main()
