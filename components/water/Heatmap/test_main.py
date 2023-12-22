import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import heatmap

# Define test data and file paths
test_data = pd.DataFrame(
    {
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Station": ["StationA", "StationB", "StationC"],
        "Percentage": [50, 75, 90],
    }
)


def test_heatmap():
    # Test the heatmap function
    date_column = "Date"
    station_column = "Station"
    percentage_column = "Percentage"
    palette = "viridis"
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.png")

        test_data.to_csv(tmp_input_file, sep=delimiter)

        heatmap(
            filepath=tmp_input_file,
            date_column=date_column,
            station_column=station_column,
            percentage_column=percentage_column,
            output=tmp_output_file,
            palette=palette,
            delimiter=delimiter,
        )

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)


if __name__ == "__main__":
    pytest.main()
