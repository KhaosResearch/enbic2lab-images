import unittest
import pandas as pd
import os
from main import main

class TestMainFunction(unittest.TestCase):

    def test_main(self):
        # Crear un archivo de entrada temporal
        input_csv = 'test_input.csv'
        with open(input_csv, 'w') as f:
            f.write("""No. of register (ID);S-P25490;S-P25492;;
Date;;;;
Authors;;;;
Group;Flora;Flora;;
Project;;;;
Community;Pino pinastri-Quercetum cocciferae;Pino halepensis-Juniperetum phoeniceae;;
Community Authors;Cabezudo,Nieto,PÃ©rez Latorre;PÃ©rez Latorre,Cabezudo;;
Community Year;1989;1998;;
Subcommunity;;;;
Subcommunity Authors;;;;
Subcommunity Year;;;;
Location;Malaga. P.N. S. de las Nieves. S. Parda de Tolox. Cerro Redondo;Malaga. P.N. S. de las Nieves.Tolox. Carril ladera S del Torrecilla. Prox. de la Loma del Moro;;
MGRS;30SUF2959;30SUF2158;;
Latitude;3.666.584.533.085.390;3.665.536.855.375.750;;
Longitude;-4.907.827.074.763.720;-49.970.628.755.605.900;;
Natural Site;Sierra de las Nieves;Sierra de las Nieves;;
Lithology;;;;
Coverage(%);80.0;100.0;;
Altitude(m);700.0;830.0;;
Plot slope;22.22;25.0;;
Alt. Veg. (cm);1.5;10.0;;
Plot area(m2);750.0;100.0;;
Plot orientation;180;180;;
Ecology;;;;
Pictures;;;;
Number of Species;11;17;;
Species;;;;
A;+;-;-;+
B;-;+;+;+
C;-;-;+;+


""")

        # Llamar a la función main
        output_csv1 = 'test_output1.csv'
        output_csv2 = 'test_output2.csv'
        main(input_csv, ';', output_csv1,output_csv2,0.05,0.85)

        # Leer el archivo de salida generado
        output_df1 = pd.read_csv(output_csv1, sep=';', header=None)
        output_df2 = pd.read_csv(output_csv2, sep=';', header=None)
        #TODO test output 2
        support = output_df1[1].values[1:]
        # Comprobar si la salida es igual a lo esperado
        expected_support = ['0.5', '0.75','0.5', '0.25','0.25', '0.5', '0.25']
        self.assertListEqual(support.tolist(), expected_support)
        '''self.assertListEqual(plot_slope.tolist(), expected_itemset)'''
        # Eliminar los archivos temporales
        os.remove(input_csv)
        os.remove(output_csv1)
        os.remove(output_csv2)

if __name__ == '__main__':
    unittest.main()