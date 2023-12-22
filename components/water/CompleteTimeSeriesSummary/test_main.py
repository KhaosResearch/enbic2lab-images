import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import complete_timeseries_summary

# Define test data and file paths
test_data_completed = pd.DataFrame(
    data={
        "DATE": ["1993-10-02", "1993-10-03", "1993-10-04", "1993-10-05"],
        "TEST-STATION": [1, 2, 3, 6.9],
    }
)

test_data_replaced = pd.DataFrame(
    data={
        "DATE": ["1993-10-03", "1993-10-05"],
        "TEST-STATION": [2, 6.9],
    }
)


def test_complete_timeseries_summary():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file_completed = os.path.join(tmp_dir, "test_completed.csv")
        tmp_input_file_replaced = os.path.join(tmp_dir, "test_replaced.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.html")

        test_data_completed.to_csv(tmp_input_file_completed, sep=delimiter, index=False)
        test_data_replaced.to_csv(tmp_input_file_replaced, sep=delimiter, index=False)

        complete_timeseries_summary(
            filepath_completed=tmp_input_file_completed,
            filepath_replaced=tmp_input_file_replaced,
            output=tmp_output_file,
            color="yellow",
            delimiter=delimiter,
        )

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        assert os.path.isfile(tmp_output_file)
        assert os.path.getsize(tmp_output_file) > 0


if __name__ == "__main__":
    pytest.main()
