import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from pandas import NA
from filecmp import cmp

from main import deleteNA

input_CSV_data = pd.DataFrame(
    data={
        "A": [1, 2, 3, 4, 5, 6, 7],
        "B": [6, 7, 8, 9, None, 11, 12],
        "C": [11, None, 13, 14, 15, 16, 17],
        "D": [16, 17, 18, 19, 20, 21, 22],
        "E": [21, 22, 23, 24, None, None, 27],
        "F": [26, 27, 28, 29, 30, 31, 32],
        "G": [31, 32, 33, 34, 35, 36, 37],
        "H": [36, 37, 38, 39, 40, 41, 42],
        "I": [41, 42, 43, 44, 45, 46, 47],
        "J": [None, None, None, None, None, None, None],
    }
)
expected_CSV_data_both = pd.DataFrame(
    data={
        "A": [1, 3, 4, 7],
        "B": [
            6.0,
            8.0,
            9.0,
            12.0,
        ],  # When a NA is present, the column type becomes a float64
        "C": [
            11.0,
            13.0,
            14.0,
            17.0,
        ],  # When a NA is present, the column type becomes a float64
        "D": [16, 18, 19, 22],
        "E": [
            21.0,
            23.0,
            24.0,
            27.0,
        ],  # When a NA is present, the column type becomes a float64
        "F": [26, 28, 29, 32],
        "G": [31, 33, 34, 37],
        "H": [36, 38, 39, 42],
        "I": [41, 43, 44, 47],
    }
)
expected_CSV_data_rows = pd.DataFrame(
    data={
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
        "H": [],
        "I": [],
        "J": [],
    }
)
expected_CSV_data_columns = pd.DataFrame(
    data={
        "A": [1, 2, 3, 4, 5, 6, 7],
        "B": [
            6.0,
            7.0,
            8.0,
            9.0,
            None,
            11.0,
            12.0,
        ],  # When a NA is present, the column type becomes a float64
        "C": [
            11.0,
            None,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
        ],  # When a NA is present, the column type becomes a float64
        "D": [16, 17, 18, 19, 20, 21, 22],
        "E": [
            21.0,
            22.0,
            23.0,
            24.0,
            None,
            None,
            27.0,
        ],  # When a NA is present, the column type becomes a float64
        "F": [26, 27, 28, 29, 30, 31, 32],
        "G": [31, 32, 33, 34, 35, 36, 37],
        "H": [36, 37, 38, 39, 40, 41, 42],
        "I": [41, 42, 43, 44, 45, 46, 47],
    }
)


def test_deleteNA_both():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)
        expected_CSV_data_both.to_csv(temp_expected_file, index=False, sep=delimiter)

        deleteNA(
            filepath=temp_input_file,
            delimiter=delimiter,
            output=temp_output_file,
            delete_option="both",
        )

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)


def test_deleteNA_rows():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)
        expected_CSV_data_rows.to_csv(temp_expected_file, index=False, sep=delimiter)

        deleteNA(
            filepath=temp_input_file,
            delimiter=delimiter,
            output=temp_output_file,
            delete_option="row",
        )

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)


def test_deleteNA_column():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)
        expected_CSV_data_columns.to_csv(temp_expected_file, index=False, sep=delimiter)

        deleteNA(
            filepath=temp_input_file,
            delimiter=delimiter,
            output=temp_output_file,
            delete_option="column",
        )

        assert os.path.exists(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
        assert cmp(temp_expected_file, temp_output_file)
