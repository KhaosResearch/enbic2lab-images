import os
import unittest
import numpy as np
import pandas as pd
from io import StringIO
from main import main  # Reemplaza "your_script_name" con el nombre real de tu script

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        # Datos de entrada para las pruebas
        self.input_data = """Date;Olea;dir
1991-05-11;134;30
1991-05-12;193;14
1991-05-13;83;17
1991-05-14;381;14
1991-05-15;234;14
1991-05-16;501;14
1991-05-17;356;14
1991-05-18;290;17
1991-05-19;28;14
1991-05-20;25;14
1991-05-21;14;12
1991-05-22;23;12
1991-05-23;17;14
1991-05-24;22;16
1991-05-25;62;16
1991-05-26;24;16
1991-05-27;14;16
1991-05-28;7;16
1991-05-29;14;16
1991-05-30;495;17
1991-05-31;211;27
1991-06-01;122;21
1991-06-02;69;27
1991-06-03;116;14"""

        # Convertir los datos de entrada a un objeto DataFrame de Pandas
        self.df = pd.read_csv(StringIO(self.input_data), sep=';', decimal=',')

    def test_main_function(self):
        # Especificar el nombre del archivo de salida para la prueba
        output_filename = "test_output.csv"

        # Llamar a la función principal con los datos de prueba
        main(StringIO(self.input_data), output_filename,";",["Olea"],["dir","olea"])

        # Cargar el resultado en un DataFrame para comparar con los datos esperados
        output_df = pd.read_csv(output_filename, sep=';', decimal=',')

        # Verificar que el DataFrame resultante tiene las columnas esperadas
        expected_columns = self.df.columns.tolist() + ['Olea_acum_3', 'Olea_acum_5', 'dir_mm_3', 'dir_mm_5']
        self.assertEqual(output_df.columns.tolist(), expected_columns)
        self.assertEqual(output_df["Olea_acum_3"][3], str(410.0))
        self.assertEqual(output_df["dir_mm_3"][3], str(20.333))

        # Puedes agregar más aserciones para verificar los resultados según tus necesidades

    def tearDown(self):
        # Limpiar archivos de salida después de cada prueba
        output_filename = "test_output.csv"
        try:
            os.remove(output_filename)
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()