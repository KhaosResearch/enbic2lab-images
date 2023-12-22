import unittest
import pandas as pd
import os
from main import main

class TestMainFunction(unittest.TestCase):

    def test_main(self):
        # Crear un archivo de entrada temporal
        input_csv = 'test_input.csv'
        with open(input_csv, 'w') as f:
            f.write("""No. of register;S-P25490;S-P25492;S-P25506;S-P25520
Date;;;;
Authors;;;;
Group;Flora;Flora;Flora;Flora
Project;;;;
Community;Pino pinastri-Quercetum cocciferae;Pino halepensis-Juniperetum phoeniceae;Cytiso baetici-Arbutetum unedi;Equiseto telmateiae-Salicetum pedicellatae
Community Authors;Cabezudo,Nieto,PÃ©rez Latorre;PÃ©rez Latorre,Cabezudo;Nieto Caldera,PÃ©rez Latorre,Cabezudo;DÃ­ez Garretas,Cuenca,Asensi
Community Year;1989;1998;1990;1986
Subcommunity;;;;
Subcommunity Authors;;;;
Subcommunity Year;;;;
Location;Malaga. P.N. S. de las Nieves. S. Parda de Tolox. Cerro Redondo;Malaga. P.N. S. de las Nieves.Tolox. Carril ladera S del Torrecilla. Prox. de la Loma del Moro;Malaga. P.N. S. de las Nieves. Istan. Albornoque. los Zarzalones;Malaga. P.N. S. de las Nieves. Istan. RÃ­o Verde. base de S. Real
MGRS;30SUF2959;30SUF2158;30SUF2856;30SUF2653
Latitude;3.666.584.533.085.390;3.665.536.855.375.750;3.663.863.591.821.710;3.661.124.419.082.040
Longitude;-4.907.827.074.763.720;-49.970.628.755.605.900;-4.918.340.159.753.060;-4.940.022.165.688.360
Natural Site;Sierra de las Nieves;Sierra de las Nieves;Sierra de las Nieves;Sierra de las Nieves
Lithology;;;;
Coverage(%);80.0;100.0;100.0;100.0
Altitude(m);700.0;830.0;650.0;260.0
Plot slope;40.0;45.0;20.0;0.0
Alt. Veg. (cm);1.5;10.0;5.0;0.035
Plot area(m2);750.0;100.0;50.0;100.0
Plot orientation;N;S;SSW;SE
Ecology;-;-;-;-
Pictures;-;-;-;-
Number of Species;11;17;19;15
Species;-;-;-;-
Cephalaria leucantha;-;-;-;-
Geum heterocarpum;-;-;-;-
""")

        # Llamar a la función main
        output_csv = 'test_output.csv'
        main(input_csv, ';', output_csv)

        # Leer el archivo de salida generado
        output_df = pd.read_csv(output_csv, sep=';', header=None)
        plot_orientation = output_df.iloc[22].values[1:]
        plot_slope = output_df.iloc[19].values[1:]

        # Comprobar si la salida es igual a lo esperado
        expected_plot_orientation = ['0', '180', '202.5', '135']
        expected_plot_slope = ['22.22', '25.0', '11.11', '0.0']

        self.assertListEqual(plot_orientation.tolist(), expected_plot_orientation)
        self.assertListEqual(plot_slope.tolist(), expected_plot_slope)

        # Eliminar los archivos temporales
        os.remove(input_csv)
        os.remove(output_csv)

if __name__ == '__main__':
    unittest.main()