import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from filecmp import cmp

from main import data_normalization

input_CSV_data = pd.DataFrame(
    {
        "pmm": [1100.0, 1100.0, 1100.0, 1100.0, 1100.0],
        "DensidadAp": [1.4024, 1.3332, 1.389, 1.4529000000000003, 1.2375],
        "Arenasmuyfinas": [
            6.999999999999993,
            6.999999999999993,
            5.55,
            7.749999999999995,
            8.85,
        ],
        "Textarenas": [35.85, 41.4, 29.1, 21.75, 35.2],
        "Textlimos": [
            44.15000000000043,
            33.60000000000054,
            48.4,
            50.749999999999254,
            44.80000000000042,
        ],
        "Textarci": [20.0, 25.0, 22.5, 27.5, 20.0],
        "ConductividadmSg": [2.31, 1.69, 3.57, 3.45, 3.94],
        "C.O.5cm": [3.39, 3.4757999999999996, 4.7, 4.5198, 4.8678],
        "M.O": [5.8308, 5.9783759999999996, 8.084, 7.774056, 8.372615999999999],
        "C.O.tha1": [
            23.77068,
            23.1696828,
            32.6415,
            32.834087100000005,
            30.119512500000006,
        ],
        "E.E": [
            66.45724859974372,
            61.833333333333336,
            87.03333333333332,
            84.7,
            49.03333333333333,
        ],
        "K.usle": [
            0.24348193330831205,
            0.17704691350417093,
            0.16688904711357389,
            0.18069974599957672,
            0.160380186894606,
        ],
        "CIC": [
            19.99380434782609,
            19.99380434782609,
            24.562282608695654,
            26.085108695652174,
            26.085108695652174,
        ],
        "Ksat": [
            14.427390791027154,
            22.5,
            14.092546109352833,
            24.742739200943532,
            23.5,
        ],
        "nespecies": [9.0, 9.0, 9.0, 9.0, 9.0],
        "cobertura": [90.0, 90.0, 90.0, 90.0, 90.0],
        "v1": [24.7, 28.3, 39.5, 39.7, 23.8],
        "v2": [1.7, 2.2, 2.2, 1.7, 1.2],
        "HumGen": [16.3725, 19.7725, 27.1575, 18.335, 14.8425],
    }
)

expected_CSV_data = pd.DataFrame(
    data={
        "pmm": [0.0, 0.0, 0.0, 0.0, 0.0],
        "DensidadAp": [
            0.5366765712073797,
            -0.4059127365984746,
            0.35415205206578293,
            1.2245488261813064,
            -1.7094647128559886,
        ],
        "Arenasmuyfinas": [
            -0.21312747667074755,
            -0.21312747667074755,
            -1.5567572208993437,
            0.4818534255164624,
            1.5011587487243725,
        ],
        "Textarenas": [
            0.4758364656373003,
            1.303702416824453,
            -0.5310275290497779,
            -1.6273905454868187,
            0.3788791920748411,
        ],
        "Textlimos": [
            -0.032285389969608745,
            -1.8249741488112958,
            0.6898878067201042,
            1.0892071037131525,
            0.07816462834765128,
        ],
        "Textarci": [
            -1.028991510855053,
            0.6859943405700353,
            -0.17149858514250882,
            1.5434872662825794,
            -1.028991510855053,
        ],
        "ConductividadmSg": [
            -0.8034234028357501,
            -1.533808314504614,
            0.6809072241041987,
            0.5395424024908706,
            1.116782090745295,
        ],
        "C.O.5cm": [
            -1.272891242558536,
            -1.1364895981918446,
            0.8096979663035355,
            0.5232227178783863,
            1.076460156568463,
        ],
        "M.O": [
            -1.2728912425585373,
            -1.136489598191846,
            0.8096979663035341,
            0.5232227178783851,
            1.0764601565684615,
        ],
        "C.O.tha1": [
            -1.1205139119142955,
            -1.2626944602650032,
            0.9780949533523464,
            1.0236561298158529,
            0.3814572890110978,
        ],
        "E.E": [
            -0.23427975874500087,
            -0.5572448148790641,
            1.2028911187745377,
            1.0399155693621682,
            -1.4512821145126404,
        ],
        "K.usle": [
            1.9404537710948415,
            -0.2905742967762157,
            -0.6316968717964097,
            -0.16790447823009683,
            -0.8502781242921202,
        ],
        "CIC": [
            -1.2001983962979579,
            -1.2001983962979579,
            0.4364357804719863,
            0.981980506061966,
            0.981980506061966,
        ],
        "Ksat": [
            -1.173642448108631,
            0.572736281199171,
            -1.2460806913779696,
            1.057916714752068,
            0.7890701435353623,
        ],
        "nespecies": [0.0, 0.0, 0.0, 0.0, 0.0],
        "cobertura": [0.0, 0.0, 0.0, 0.0, 0.0],
        "v1": [
            -0.9256292035437043,
            -0.4129730292733448,
            1.181957290678884,
            1.21043818924946,
            -1.0537932471112939,
        ],
        "v2": [
            -0.26726124191242456,
            1.0690449676496976,
            1.0690449676496976,
            -0.26726124191242456,
            -1.6035674514745462,
        ],
        "HumGen": [
            -0.6840238102076995,
            0.11148874484828793,
            1.8393888092860708,
            -0.22484928394376535,
            -1.0420044599828935,
        ],
    }
)


def test_data_normalization():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "DataNormalized.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=";")
        expected_CSV_data.to_csv(temp_expected_file, index=False, sep=";")

        data_normalization(temp_input_file, delimiter, temp_output_file)

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)
