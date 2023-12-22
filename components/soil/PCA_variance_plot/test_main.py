import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd

from main import pca_variance_plot

input_scree_plot_data = pd.DataFrame(
    data={
        "": [
            54.7,
            10.0,
            6.5,
            5.3,
            4.6,
            4.0,
            3.1,
            2.9,
            2.4,
            1.8,
            1.6,
            1.1,
            0.8,
            0.4,
            0.3,
            0.2,
            0.1,
            0.1,
            0.1,
        ]
    }
)


def test_scatter_plot():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output_plot.pdf")

        input_scree_plot_data.to_csv(temp_input_file, index=False, sep=";")

        pca_variance_plot(
            filepath=temp_input_file,
            delimiter=delimiter,
            output=temp_output_file,
        )

        assert os.path.isfile(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
