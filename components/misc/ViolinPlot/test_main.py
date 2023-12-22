import pytest
import os
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

from main import violinplot

# Define test data and file paths
size = 1000
test_data_1 = pd.DataFrame(
    data={
        "DATA1": np.random.choice(range(1, 100), size),
        "DATA2": np.random.choice(range(1, 100), size),
        "DATA3": np.random.choice(["orange", "apple", "banana"], size),
        "DATA4": np.random.choice(["fresh", "rotten"], size),
    }
)


def test_homogeneity_plot():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")

        test_data_1.to_csv(tmp_input_file, sep=delimiter, decimal=".", index=False)

        violinplot(
            filepath=tmp_input_file,
            output_path=tmp_dir,
            x_column="DATA3",
            y_column="DATA1",
            hue="DATA4",
            split=True,
            inner="quartile",
            orient="horizontal",
            palette="Set2",
            title="Test Title",
            delimiter=delimiter,
        )

        # mpimg.imread(os.path.join(tmp_dir, "violinplot.png"))
        # plt.show()

        assert os.path.exists(os.path.join(tmp_dir, "treeplot.pdf"))
        assert os.path.exists(os.path.join(tmp_dir, "treeplot.png"))
        assert os.path.exists(os.path.join(tmp_dir, "treeplot.svg"))


if __name__ == "__main__":
    pytest.main()
