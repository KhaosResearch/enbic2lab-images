import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd

from main import pca_scatter_plot

input_PCA_data = pd.DataFrame(
    data={
        "PC1": [
            -0.8737201986502987,
            -1.1435042484378979,
            2.116629271498637,
            1.519587180198323,
            -1.6189920046087631,
        ],
        "PC2": [
            -0.8702901745109689,
            -1.278826097326873,
            -0.23752402665487585,
            0.6831016721048037,
            1.703538626387915,
        ],
    }
)


def test_scatter_plot():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output_plot.pdf")

        input_PCA_data.to_csv(temp_input_file, index=False, sep=";")

        pca_scatter_plot(
            filepath=temp_input_file,
            delimiter=delimiter,
            x_axis="PC1",
            y_axis="PC2",
            output=temp_output_file,
        )

        assert os.path.isfile(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
