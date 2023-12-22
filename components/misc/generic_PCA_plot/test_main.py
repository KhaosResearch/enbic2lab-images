import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import generic_pca_plot

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
        generic_pca_plot(
            filepath=tmp_input_file,
            color_list=["red", "green", "blue"],
            target_column="DATA3",
            output_path=tmp_dir,
            title="Test title",
            x_label="Test x label",
            y_label="Test y label",
            delimiter=delimiter,
        )

        assert os.path.exists(os.path.join(tmp_dir, "pca_plot.pdf"))
        assert os.path.exists(os.path.join(tmp_dir, "pca_plot.png"))
        assert os.path.exists(os.path.join(tmp_dir, "pca_plot.svg"))


if __name__ == "__main__":
    pytest.main()
