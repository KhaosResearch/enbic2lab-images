import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import jointplot

# Define test data and file paths
test_data_1 = pd.DataFrame(
    data={
        "DATA1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "DATA2": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "DATA3": [
            "Apple",
            "Banana",
            "Orange",
            "Apple",
            "Banana",
            "Orange",
            "Apple",
            "Banana",
            "Orange",
            "Apple",
        ],
        "DATA4": [
            "01-02-2003",
            "17-12-2016",
            "31-01-2000",
            "01-02-2003",
            "17-12-2016",
            "31-01-2000",
            "01-02-2003",
            "17-12-2016",
            "31-01-2000",
            "01-02-2003",
        ],
    }
)


def test_homogeneity_plot():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")

        test_data_1.to_csv(tmp_input_file, sep=delimiter, decimal=".", index=False)
        jointplot(
            filepath=tmp_input_file,
            x_column="DATA1",
            y_column="DATA2",
            title="Test",
            x_label="X",
            y_label="Y",
            delimiter=delimiter,
            output_path=tmp_dir,
        )

        assert os.path.exists(os.path.join(tmp_dir, "jointplot.pdf"))
        assert os.path.exists(os.path.join(tmp_dir, "jointplot.png"))
        assert os.path.exists(os.path.join(tmp_dir, "jointplot.svg"))


if __name__ == "__main__":
    pytest.main()
