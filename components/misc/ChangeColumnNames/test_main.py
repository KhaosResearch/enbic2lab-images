import unittest
from tempfile import NamedTemporaryFile
from pathlib import Path
import pandas as pd
from main import rename_columns

class TestRenameColumns(unittest.TestCase):
    def test_rename_columns(self):
        # Create a temporary CSV file for testing
        with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
            temp_file.write("A;B;C\n1;2;3\n4;5;6\n")
            temp_file_path = Path(temp_file.name)

        # Define expected and actual column names
        expected_columns = ["J", "Q", "K"]

        try:
            # Read CSV file and call the rename_columns function
            df = pd.read_csv(temp_file_path, sep=";")
            df_renamed = rename_columns(df, labels=expected_columns)
            # Check if the columns are renamed correctly
            self.assertListEqual(df_renamed.columns.tolist(), expected_columns)
        finally:
            # Clean up the temporary file
            temp_file_path.unlink()

if __name__ == '__main__':
    unittest.main()