import pytest
import os
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

from main import train_test_splitter

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


def test_train_test_splitter():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file = os.path.join(tmp_dir, "test_input.csv")

        test_data_1.to_csv(tmp_input_file, sep=delimiter, decimal=".", index=False)

        train_test_splitter(
            filepath=tmp_input_file,
            output_path=tmp_dir,
            target_column="DATA4",
            predict_split=0.1,
            train_split=0.8,
            delimiter=delimiter,
        )

        assert os.path.exists(os.path.join(tmp_dir, "predict.csv"))
        assert os.path.exists(os.path.join(tmp_dir, "train.csv"))
        assert os.path.exists(os.path.join(tmp_dir, "test.csv"))

        assert os.path.getsize(os.path.join(tmp_dir, "predict.csv")) > 0
        assert os.path.getsize(os.path.join(tmp_dir, "train.csv")) > 0
        assert os.path.getsize(os.path.join(tmp_dir, "test.csv")) > 0


if __name__ == "__main__":
    pytest.main()
