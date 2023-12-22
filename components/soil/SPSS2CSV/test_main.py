import os
from tempfile import TemporaryDirectory

import pytest
import pyreadstat
import pandas as pd
from filecmp import cmp

from main import spss2csv

sample_SAV_data = pd.DataFrame(
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


def test_ssps2csv():
    drop_index = True
    with TemporaryDirectory() as temp_dir:
        temp_sav_file = os.path.join(temp_dir, "input_test.sav")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "Data.csv")

        pyreadstat.write_sav(sample_SAV_data, temp_sav_file)
        sample_SAV_data.to_csv(temp_expected_file, index=False, sep=";")

        spss2csv(temp_sav_file, drop_index, temp_output_file)

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)
