import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import plot_highlight_summary

# Define test data and file paths
test_data_1 = pd.DataFrame(
    data={
        "Hidrologic Year": ["2012/2013", "2013/2014", "2014/2015"],
        "Station": ["STATION1", "STATION2", "STATION3"],
        "Sum of the Year": [4, 5, 6],
    }
)


def test_plot_highlight_summary():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file_precipitations = os.path.join(
            tmp_dir, "test_input_precipitations.csv"
        )
        tmp_output_file = os.path.join(tmp_dir, "test_output.html")

        test_data_1.to_csv(
            tmp_input_file_precipitations, sep=delimiter, decimal=".", index=False
        )

        plot_highlight_summary(
            filepath=tmp_input_file_precipitations,
            output=tmp_output_file,
            delimiter=delimiter,
        )

        with open(tmp_output_file) as f:
            html_content = f.read()
            assert "STATION1" in html_content
            assert "STATION2" in html_content
            assert "STATION3" in html_content
            assert "2012/2013" in html_content
            assert "2013/2014" in html_content
            assert "2014/2015" in html_content
            assert "table" in html_content

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        assert os.path.isfile(tmp_output_file)
        assert os.path.getsize(tmp_output_file) > 0


if __name__ == "__main__":
    pytest.main()
