import pytest
import os
import pandas as pd
import numpy as np
from tempfile import TemporaryDirectory

from main import random_forest_regressor

# Define test data and file paths
size = 1000
test_data_1 = pd.DataFrame(
    data={
        "DATA1": np.random.choice(range(1, 151), size),
        "DATA2": np.random.choice(range(1, 99), size),
        "DATA3": np.random.choice(range(0,20), size),
        "DATA4": np.random.choice(range(1, 200), size),
    }
)


def test_kneighbours():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_train = os.path.join(tmp_dir, "train_input.csv")
        tmp_input_test = os.path.join(tmp_dir, "test_input.csv")

        train_data = test_data_1.iloc[range(0, int(size * 0.8)), :]
        test_data = test_data_1.iloc[range(int(size * 0.8), size), :]
        train_data.to_csv(tmp_input_train, sep=delimiter, decimal=".", index=False)
        test_data.to_csv(tmp_input_test, sep=delimiter, decimal=".", index=False)

        random_forest_regressor(
            filepath_train=tmp_input_train,
            filepath_test=tmp_input_test,
            target_column="DATA3",
            delimiter=delimiter,
            output=tmp_dir,
        )
        
        assert os.path.exists(os.path.join(tmp_dir, "model.onnx"))
        assert os.path.exists(os.path.join(tmp_dir, "metrics.png"))
        assert os.path.getsize(os.path.join(tmp_dir, "model.onnx")) > 0


if __name__ == "__main__":
    pytest.main()