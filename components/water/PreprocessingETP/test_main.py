import os
from filecmp import cmp
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from main import main

"Fecha", "TMAX", "TMIN"
input_data = pd.DataFrame(
    data={
        "Fecha": [
            "01/10/2003",
            "02/10/2003",
            "03/10/2003",
            "04/10/2003",
            "05/10/2003",
            "06/10/2003",
            "07/10/2003",
            "08/10/2003",
            "09/10/2003",
        ],
        "TMAX": [20.99, 19.49, 22.47, 21.63, 21.63, 19.72, 21.54, 25.90, 24.99],
        "TMIN": [16.50, 15.68, 15.10, 15.05, 15.73, 15.63, 14.58, 14.36, 13.58],
        "Latitud": [36.62, 36.62, 36.62, 36.62, 36.62, 36.62, 36.62, 36.62, 36.62],
    }
)


def test_preprocessing_etp():

    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.xlsx")
        temp_output_file = os.path.join(temp_dir, "output_test.csv")

        df = pd.DataFrame(input_data)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df.to_excel(temp_input_file, index=False)

        main(temp_input_file, "37.59", "0.01745", "0.175", temp_output_file)
        df_final = pd.read_csv(temp_output_file, sep=";")

        assert df_final["TMedia"][0] == 18.745  # expected number for this row
        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
