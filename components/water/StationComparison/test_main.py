import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import station_comparison

# Define test data and file paths
test_data_1 = pd.DataFrame(
    data={
        "DATE": ["2019-01-01", "2019-01-02", "2019-01-03"],
        "STATION1": [1, 2, 3],
        "STATION2": [4, 5, 6],
        "STATION3": [7, 8, 9],
    }
)


def test_station_comparison():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file_precipitations = os.path.join(
            tmp_dir, "test_input_precipitations.csv"
        )
        tmp_input_file_analysis = os.path.join(tmp_dir, "test_input_analysis.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.html")

        test_data_1.to_csv(
            tmp_input_file_precipitations, sep=delimiter, decimal=".", index=False
        )

        station_comparison(
            filepath=tmp_input_file_precipitations,
            stationA="STATION1",
            stationB="STATION2",
            output=tmp_output_file,
            delimiter=delimiter,
        )

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        assert os.path.isfile(tmp_output_file)
        assert os.path.getsize(tmp_output_file) > 0


if __name__ == "__main__":
    pytest.main()
