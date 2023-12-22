import pytest
import os
from tempfile import TemporaryDirectory
import pandas as pd

from main import sklearn_predictor


def test_train_test_splitter():
    delimiter = ","

    with TemporaryDirectory() as tmp_dir:
        sklearn_predictor(
            filepath_model="./test_resources/test_model_kmeans.onnx",
            filepath_data="./test_resources/predict_test.csv",
            output=tmp_dir,
            delimiter=delimiter,
        )
        input = pd.read_csv("./test_resources/predict_test.csv", sep=delimiter, decimal=".", header=0)
        output = pd.read_csv(f"{tmp_dir}/predictions.csv", sep=delimiter, decimal=".", header=0)

        assert os.path.exists(f"{tmp_dir}/predictions.csv")
        assert output.columns.tolist()[-1] == "prediction"
        assert output.shape[0] == input.shape[0]
        assert output.shape[1] == input.shape[1] + 1


if __name__ == "__main__":
    pytest.main()
