import unittest
import os
import numpy as np
from main import split_sequences_multivariable
from numpy import savetxt, loadtxt
import tempfile
from pathlib import Path


class TestSplitSequencesMultivariable(unittest.TestCase):

    def setUp(self):
        # Guardar los datos en archivos temporales
        self.temp_dir = tempfile.TemporaryDirectory()
        self.sequences_x = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        self.sequences_y = np.array([10, 20, 30, 40])

    def test_split_sequences_multivariable(self):
        # Crear un archivo temporal con los datos de ejemplo

        features = os.path.join(self.temp_dir.name, "features.csv")
        savetxt(features, self.sequences_x, delimiter=";")
        target = os.path.join(self.temp_dir.name, "target.csv")
        savetxt(target, self.sequences_y, delimiter=";")

        split_sequences_multivariable(features, target, n_steps_in=2, n_steps_out=1, delimiter=";",
                                      output_path=self.temp_dir.name
        )
        output_x = os.path.join(self.temp_dir.name, "sequenceX.npy")
        output_y = os.path.join(self.temp_dir.name, "sequenceY.npy")

        # Verificar si los archivos de salida existen
        self.assertTrue(os.path.exists(output_x))
        self.assertTrue(os.path.exists(output_y))

        # Cargar los datos de los archivos de salida
        loaded_x = np.load(output_x)
        loaded_y = np.load(output_y)

        expected_output_x = np.array([[[1, 2], [3, 4]], [[3, 4], [5, 6]], [[5, 6], [7, 8]]])
        expected_output_y = np.array([[20], [30], [40]])

        # Verificar si los datos cargados coinciden con los datos originales
        np.testing.assert_array_equal(loaded_x,expected_output_x)
        np.testing.assert_array_equal(loaded_y, expected_output_y)

    def tearDown(self):
        self.temp_dir.cleanup()

if __name__ == "__main__":
    unittest.main()

