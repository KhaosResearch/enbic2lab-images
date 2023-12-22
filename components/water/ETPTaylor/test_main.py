import pytest
import os
import pandas as pd
from math import isclose
from tempfile import TemporaryDirectory

from main import main

# Define test data and file paths
input_data = pd.DataFrame(
    data = {
        'Fecha': ['01/10/2003', '02/10/2003', '03/10/2003', '04/10/2003', '05/10/2003'],
        'TMAX': [20.988489151000977, 19.494600296020508, 22.46558952331543, 21.634719848632812, 21.634719848632812],
        'TMIN': [16.50489044189453, 15.676690101623535, 15.103320121765137, 15.04757022857666, 15.732430458068848],
        'TMedia': [18.746689796447754, 17.58564519882202, 18.784454822540283, 18.341145038604736, 18.68357515335083],
        'Latitud': [36.62, 36.62, 36.62, 36.62, 36.62],
        'Día juliano': [274, 275, 276, 277, 278],
        'Distancia Tierra-Sol': [1.0001419843818353, 1.0007099987224948, 1.0012778026752973, 1.0018452279877477, 1.0024121065195493],
        'Declinación diaria en grados': [-4.215480336817683, -4.611933236708873, -5.0070195218169715, -5.400622119597755, -5.792624397155389],
        'Latitud RAD': [0.6391395720803235, 0.6391395720803235, 0.6391395720803235, 0.6391395720803235, 0.6391395720803235],
        'Declinación RAD': [-0.07357401143054812, -0.08049341986272884, -0.08738897636733821, -0.0942586376430158, -0.10110036806171319],
        '(menos)Tangente': [-0.743207275850095, -0.743207275850095, -0.743207275850095, -0.743207275850095, -0.743207275850095],
        'Tangente declinación': [-0.07370705486681263, -0.0806677156658486, -0.08761211637039695, -0.09453878624794124, -0.10144624077497312],
        'Multiplicación': [0.054779619458497304, 0.05995283320906537, 0.06511396233910424, 0.07026191378950683, 0.0753955842516006],
        'Angulo horario (radianes)': [1.5159892730991276, 1.5108075202036115, 1.5056362644451504, 1.5004764734389018, 1.4953291282413566],
        'Angulo horario (Grados)': [86.85978713568555, 86.56289456429279, 86.26660343455025, 85.97096918672264, 85.67604803120636],
        'CTE1': [37.59, 37.59, 37.59, 37.59, 37.59],
        'CTE2': [0.01745, 0.01745, 0.01745, 0.01745, 0.01745],
        'Seno latitud': [0.5965050748005212, 0.5965050748005212, 0.5965050748005212, 0.5965050748005212, 0.5965050748005212],
        'Seno declinación': [-0.07350765171580186, -0.08040652598216504, -0.08727778965901344, -0.09411912315994347, -0.10092822679098788],
        'Coseno latitud': [0.8026093045418952, 0.8026093045418952, 0.8026093045418952, 0.8026093045418952, 0.8026093045418952],
        'Coseno declinación': [0.9972946531187402, 0.9967621534646465, 0.9961840128371048, 0.9955609427130031, 0.9948937094166527],
        'Seno ángulo horario': [0.9984984693488429, 0.9982012110743034, 0.9978778341603253, 0.9975285777714019, 0.9971537022321884],
        'tmax-tmin^0.5': [2.1174509933187227, 1.9539473366488087, 2.7133502172683666, 2.5665442953621804, 2.4294627781803873],
        'tmax-tmin^0.99': [4.416827804682881, 3.7671026244526638, 7.2167487910424715, 6.464137008448916, 5.798428339399399],
        'tmax-tmin^0.75': [3.0812011521872416, 2.7312992248939514, 4.46949832534757, 4.111716342362673, 3.7867390166770343],
        'tmax-tmin^0.25': [1.455146382093129, 1.3978366630793486, 1.6472250050519408, 1.602043786967816, 1.5586734033082066],
        'tmax-tmin^0.01': [1.0151173890801837, 1.0134871743643274, 1.0201642893110596, 1.0190300130468233, 1.0179119314899259],
        'KT': [0.175, 0.175, 0.175, 0.175, 0.175],
        'Ro': [27.548960887301433, 27.314323673675034, 27.07976181828133, 26.845364592614004, 26.61122177815869],
        'Ro EXTRATERRESTRE mm/dia': [11.239976042018984, 11.144244058859414, 11.048542821858781, 10.952908753786513, 10.857378485488745],
        'Rs': [4.165017226134054, 3.8106715496102153, 5.24624906158314, 4.9194469589393215, 4.616079457344504],
        'Ravanazzi': [1.9085029623776457, 1.6906309811108917, 2.4064327369085263, 2.229171651338722, 2.1115348012561324]
    }
)

expected_data = [2.498992641249351, 2.2863865928955827, 3.1477271556457866, 2.9516472094931765, 2.769628054036091]


def test_etp():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.csv")

        input_data.to_csv(tmp_input_file, sep=delimiter, index=False)

        main(
            filepath=tmp_input_file,
            delimiter=delimiter,
            output=tmp_output_file,
        )
        
        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        
        # Check if the output file has the expected results
        output = pd.read_csv(tmp_output_file, delimiter=delimiter)
        for i in range(len(output)):
            assert isclose(output.iloc[i]["ETP Taylor"], expected_data[i])


if __name__ == "__main__":
      pytest.main()