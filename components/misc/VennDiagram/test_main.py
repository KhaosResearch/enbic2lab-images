import unittest
import pandas as pd
from main import main
import os

class TestYourScript(unittest.TestCase):
    def test_main_function(self):
        # Crear un DataFrame de prueba
        test_data = {
            "Alcornocales": ["a", "b", "c"],
            "Cabo de Gata": ["b", "c", "d"],
            "Sierra de las Nieves": ["c", "a", "e"],
        }
        test_df = pd.DataFrame(test_data)

        # Especificar rutas de salida de prueba
        test_output1_path = "test_output1.csv"
        test_output2_path = "test_output2.pdf"
        test_csv_path = "test_input.csv"

        # Guardar el DataFrame como un archivo CSV
        test_df.to_csv(test_csv_path, index=False)

        # Llamar a la función principal con los argumentos de prueba
        main(test_csv_path, test_output1_path, test_output2_path, delimiter=",", legend="True")

        # Leer el resultado del archivo CSV generado por tu función principal
        result_df = pd.read_csv(test_output1_path, sep=";")
        # Verificar si el DataFrame resultante tiene el formato esperado
        # Asertar que la segunda columna es "Natural Sites"
        self.assertEqual(result_df.columns[1], "Alcornocales")
        self.assertEqual(result_df.columns[2], "Sierra de las Nieves")
        self.assertEqual(result_df.columns[3], "Cabo de Gata")
        self.assertEqual(result_df["Alcornocales"][0], "Alcornocales")
        self.assertTrue(pd.isna(result_df["Sierra de las Nieves"][1]))
        self.assertTrue(pd.isna(result_df["Cabo de Gata"][0]))
        self.assertEqual(result_df["Cabo de Gata"][1], "Cabo de Gata")



        # Verificar si el archivo PDF se ha generado correctamente
        pdf_generated = os.path.exists(test_output2_path)
        self.assertTrue(pdf_generated, "El archivo PDF no se generó correctamente")

        # Limpiar archivos de prueba después de la prueba
        os.remove(test_csv_path)
        os.remove(test_output1_path)
        os.remove(test_output2_path)

if __name__ == "__main__":
    unittest.main()