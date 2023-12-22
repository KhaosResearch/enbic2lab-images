import pytest
import os
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory

from main import encode_categorical_data

# Define test data and file paths
size = 1000
test_data_1 = pd.DataFrame(
    data={
        "DATA1": np.random.choice(range(1, 151), size),
        "DATA2": np.random.choice(range(1, 99), size),
        "DATA3": np.random.choice(["orange", "apple", "banana", "strawberry"], size),
        "DATA4": np.random.choice(range(1, 200), size),
    }
)


def test_encode_categorical_data_output_types():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input = os.path.join(tmp_dir, "test_input.csv")

        test_data_1.to_csv(tmp_input, index=False, sep=delimiter, decimal=".")

        encode_categorical_data(
            filepath=tmp_input,
            output=tmp_dir,
            delimiter=delimiter,
            exclude_columns=None,
        )

        output = pd.read_csv(os.path.join(tmp_dir, "output.csv"), delimiter=delimiter)

        assert os.path.exists(
            os.path.join(tmp_dir, "output.csv")
        ), "Output file does not exist"
        assert all(output[col].dtype.kind in ["i", "u", "f"] for col in output.columns)


if __name__ == "__main__":
    pytest.main()
