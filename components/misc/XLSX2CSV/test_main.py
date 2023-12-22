import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from filecmp import cmp

from main import xlsx2csv

input_data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank"],
    "Age": [25, 30, 28, 35, 29, 40],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "Seattle"],
    "Salary": [55000, 65000, 60000, 75000, 59000, 80000],
    "Department": ["HR", "Finance", "Marketing", "Engineering", "Sales", "IT"],
}


def test_xlsx2xsv():
    delimiter = ";"
    header = True
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.xlsx")
        temp_expected_file = os.path.join(temp_dir, "expected_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        # Create input file
        input_df = pd.DataFrame(input_data)
        writer = pd.ExcelWriter(temp_input_file, engine="openpyxl")
        input_df.to_excel(writer, index=False)
        writer.close()

        # Create expected file
        expected_df = pd.DataFrame(input_data)
        expected_df.to_csv(temp_expected_file, sep=delimiter, index=False)

        # Run test
        xlsx2csv(
            filepath=temp_input_file,
            delimiter=delimiter,
            header=header,
            output=temp_output_file,
        )

        assert os.path.exists(temp_output_file) == True
        assert os.path.getsize(temp_output_file) > 0

        # Compare output with expected
        assert cmp(temp_output_file, temp_expected_file) == True
