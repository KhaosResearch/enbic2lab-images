import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

from main import relplot

# Define test data and file paths
test_data_1 = pd.DataFrame(
    data={
        "DATA1": [0.5, 4, 7.3, 1.2, 9.65, 0.785, 6.1, 3.2, 2.5, 1.5],
        "DATA2": [2.7, 3.2, 1.5, 0.5, 4, 7.3, 1.2, 9.65, 0.785, 6.1],
        "DATA3": [
            "Orange",
            "Orange",
            "Orange",
            "Apple",
            "Apple",
            "Orange",
            "Apple",
            "Banana",
            "Banana",
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

        relplot(
            filepath=tmp_input_file,
            x_column="DATA1",
            y_column="DATA2",
            hue="DATA3",
            kind="scatter",
            style="DATA4",
            output_path=tmp_dir,
            delimiter=delimiter,
        )

        # mpimg.imread(os.path.join(tmp_dir, "relplot.png"))
        # plt.show()

        assert os.path.exists(os.path.join(tmp_dir, "relplot.pdf"))
        assert os.path.exists(os.path.join(tmp_dir, "relplot.png"))
        assert os.path.exists(os.path.join(tmp_dir, "relplot.svg"))


if __name__ == "__main__":
    pytest.main()
