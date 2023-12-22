import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from filecmp import cmp

from main import split_dataset

input_CSV_data = pd.DataFrame(
    data = {
        "A": [1, 2, 3, 4, 5, 6, 7],
        "B": [6, 7, 8, 9, 10, 11, 12],
        "C": [11, 12, 13, 14, 15, 16, 17],
        "D": [16, 17, 18, 19, 20, 21, 22],
        "E": [21, 22, 23, 24, 25, 26, 27],
        "F": [26, 27, 28, 29, 30, 31, 32],
        "G": [31, 32, 33, 34, 35, 36, 37],
        "H": [36, 37, 38, 39, 40, 41, 42],
        "I": [41, 42, 43, 44, 45, 46, 47],
        "J": [46, 47, 48, 49, 50, 51, 52]
    }
)


def test_split_dataset():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)
        input_CSV_data[["A", "B", "F", "G", "J"]].to_csv(temp_expected_file, index=False, sep=delimiter)

        split_dataset(
            filepath=temp_input_file,
            attribute_list=["A", "B", "F", "G", "J"],
            delimiter=delimiter,
            output=temp_output_file
        )

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)

def test_split_dataset_attribute_error():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=";")

        with pytest.raises(ValueError) as err_info:
            split_dataset(
                filepath=temp_input_file,
                attribute_list=["A", "B", "F", "G", "J", "Z"],
                delimiter=delimiter,
                output=temp_output_file
            )
        
        assert f"Not all attributes in list are in the dataframe. Possible values for this dataset: {', '.join(input_CSV_data.columns)}" in str(err_info.value)
        assert not os.path.exists(temp_output_file)
