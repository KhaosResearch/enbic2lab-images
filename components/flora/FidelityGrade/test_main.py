import unittest
import pandas as pd
from main import neighbors_species

class TestSpeciesGraph(unittest.TestCase):

    def test_neighbors_species(self):
        # Crear un DataFrame de prueba
        data = {
            "S-P1": ['', 1, '-',1],  
            "S-P2": ['', '-', 1,'-'],  
            "S-P3": ['', '-', 1,1]
        }

        index = ["Species", "Cep", "Ge", "Pa"]

        df = pd.DataFrame(data, index=index)

        df.index.name = "No. of register (ID)"
        result = neighbors_species(df.T, ['Cep'])

        self.assertIn('Cep', result[0])
        self.assertEqual(result[0]['Cep'], ['Cep', 'Species', 'a'])

if __name__ == '__main__':
    unittest.main()
