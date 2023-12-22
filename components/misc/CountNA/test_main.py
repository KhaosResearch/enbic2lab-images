import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from filecmp import cmp

from main import count_na

input_data = pd.DataFrame(
    data={
        "DATE": [
            "1988-05-12",
            "1988-05-13",
            "1988-06-03",
            "1988-06-04",
            "1988-06-05",
            "1988-06-06",
            "1988-06-07",
            "1988-06-08",
            "1988-06-09",
            "1988-06-10",
            "1988-06-11",
            "1988-06-12",
            "1989-05-23",
            "1989-05-24",
            "1989-05-25",
            "1989-05-26",
            "1989-05-27",
            "1989-05-28",
            "1989-05-29",
            "1989-05-30",
            "1989-05-31",
            "1989-06-01",
            "1989-06-02",
            "1989-06-03",
            "1989-06-04",
            "1989-06-05",
            "1989-06-06",
            "1989-06-07",
            "1989-06-08",
            "1989-06-9",
            "1989-06-10",
            "1989-06-11",
            "1989-06-12",
            "1989-06-13",
            "1989-06-14",
            "1989-06-15",
            "1989-06-16",
            "1989-06-17",
            "1989-06-18",
            "1989-06-19",
            "1989-06-20",
            "1989-06-21",
            "1989-06-22",
            "1989-06-23",
            "1989-06-24",
            "1989-06-25",
            "1989-06-26",
            "1989-06-27",
            "1989-06-28",
        ],
        "JABUGO": [
            4.7,
            0.0,
            0.0,
            None,
            0.0,
            0.0,
            0.0,
            0.0,
            6.0,
            21.0,
            8.5,
            2.0,
            0.0,
            None,
            14.5,
            8.3,
            None,
            2.5,
            19.0,
            2.4,
            12.2,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            None,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        "GALAROZA": [
            7.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            4.0,
            4.5,
            15.0,
            21.0,
            0.0,
            1.7,
            0.0,
            7.7,
            14.0,
            7.5,
            9.0,
            11.0,
            2.2,
            10.0,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0.0,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        "CORTEGANA": [
            10.3,
            0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            None,
            5.5,
            4.2,
            10.0,
            20.5,
            0.0,
            1.6,
            21.3,
            3.6,
            12.0,
            3.7,
            29.2,
            3.2,
            5.6,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            None,
        ],
        "ARACENA": [
            9.0,
            None,
            None,
            0.0,
            0.0,
            0.0,
            0.0,
            11.0,
            2.0,
            10.0,
            19.0,
            None,
            0.0,
            10.0,
            0.0,
            4.0,
            11.0,
            3.0,
            8.0,
            0.0,
            14.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            None,
            0.0,
            None,
            0.0,
            0.0,
            None,
            0.0,
            None,
            0.0,
            0.0,
            0.0,
            None,
            0.0,
            None,
            0.0,
            0.0,
            None,
            0.0,
            0.0,
            None,
            0.0,
            None,
            None,
        ],
        "ALAJAR": [
            16.3,
            0.0,
            0.0,
            0.0,
            None,
            None,
            0.0,
            8.0,
            5.7,
            7.2,
            7.0,
            4.5,
            0.5,
            1.0,
            13.6,
            2.8,
            7.2,
            4.0,
            32.2,
            0.7,
            18.2,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            None,
        ],
    }
)


def test_count_na():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output_test.csv")

        pd.DataFrame(input_data).to_csv(temp_input_file, index=False, sep=delimiter)

        count_na(temp_input_file, temp_output_file, delimiter)

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
