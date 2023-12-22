import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import clustermap

# Define test data and file paths
test_data = pd.DataFrame(
    {
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Station": ["StationA", "StationB", "StationC"],
        "Sum": [50, 75, 90],
    }
)


def test_clustermap():
    # Test the clustermap function
    date_column = "Date"
    station_column = "Station"
    square_column = "Sum"
    palette = "viridis"
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.png")

        test_data.to_csv(tmp_input_file, sep=delimiter)

        clustermap(
            filepath=tmp_input_file,
            date_column=date_column,
            station_column=station_column,
            square_column=square_column,
            output=tmp_output_file,
            palette=palette,
            delimiter=delimiter,
            drop_na=False,
        )

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)


if __name__ == "__main__":
    pytest.main()
