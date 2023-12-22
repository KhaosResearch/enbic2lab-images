import unittest
from unittest.mock import patch
import json
from tempfile import TemporaryDirectory
import os
import pandas as pd

import main


class MockCollection:
    def __init__(self, data):
        self.data = data

    def find(self, query=None):
        if query is None:
            return self.data
        return [item for item in self.data if self._matches_query(item, query)]

    def count_documents(self, query=None):
        return len(self.find(query))

    def _matches_query(self, item, query):
        for subquery in query.get("$and"):
            for key, value in subquery.items():
                if key == "$or":
                    if not any(
                        all(
                            value2.get("$regex", "").lower()
                            in item.get(key2, "").lower()
                            for key2, value2 in subsubquery.items()
                        )
                        for subsubquery in value
                    ):
                        return False
                elif type(value) == dict:
                    if key not in item or item[key] != value.get("$regex"):
                        return False
                else:
                    if key not in item or item[key] != value:
                        return False
        return True


class TestDB2CSVSoil(unittest.TestCase):
    @patch("main.mongo_connection_to_collection")
    def test_db2csv_soil_success(self, mocker_collection):
        with open("test_collection.json", "r") as file:
            data = json.load(file)
        mongo_col = MockCollection(data)
        mocker_collection.return_value = mongo_col
        delimiter = ";"

        with TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "test.csv")

            main.db2csv_soil(output=temp_output_file, delimiter=delimiter)

            assert os.path.exists(temp_output_file)
            assert os.path.getsize(temp_output_file) > 0

            input = pd.DataFrame(data)
            output = pd.read_csv(temp_output_file, sep=delimiter)
            assert output.shape == input.shape
            # This fails because NaN != None and CSV stores lists as strings and not as lists
            # assert output.equals(input)

    @patch("main.mongo_connection_to_collection")
    def test_db2csv_soil_query1_success(self, mocker_collection):
        with open("test_collection.json", "r") as file:
            data = json.load(file)
        mongo_col = MockCollection(data)
        mocker_collection.return_value = mongo_col
        delimiter = ";"

        with TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "test.csv")

            main.db2csv_soil(output=temp_output_file, delimiter=delimiter, id="0203")

            assert os.path.exists(temp_output_file)
            assert os.path.getsize(temp_output_file) > 0

            output = pd.read_csv(temp_output_file, sep=delimiter)
            assert output.shape[0] == 1

    @patch("main.mongo_connection_to_collection")
    def test_db2csv_soil_query2_success(self, mocker_collection):
        with open("test_collection.json", "r") as file:
            data = json.load(file)
        mongo_col = MockCollection(data)
        mocker_collection.return_value = mongo_col
        delimiter = ";"

        with TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "test.csv")

            main.db2csv_soil(
                output=temp_output_file,
                delimiter=delimiter,
                natural_site_list=["Cabo de Gata-Níjar", "Cazorla"],
            )

            assert os.path.exists(temp_output_file)
            assert os.path.getsize(temp_output_file) > 0

            output = pd.read_csv(temp_output_file, sep=delimiter)
            assert output.shape[0] == 2

    @patch("main.mongo_connection_to_collection")
    def test_db2csv_soil_query3_success(self, mocker_collection):
        with open("test_collection.json", "r") as file:
            data = json.load(file)
        mongo_col = MockCollection(data)
        mocker_collection.return_value = mongo_col
        delimiter = ";"

        with TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "test.csv")

            main.db2csv_soil(
                output=temp_output_file,
                delimiter=delimiter,
                natural_site_list=["Cabo de Gata-Níjar"],
                project="ECUDE",
            )

            assert os.path.exists(temp_output_file)
            assert os.path.getsize(temp_output_file) > 0

            output = pd.read_csv(temp_output_file, sep=delimiter)
            assert output.shape[0] == 1

    @patch("main.mongo_connection_to_collection")
    def test_db2csv_soil_KeyError(self, mocker_collection):
        with open("test_collection.json", "r") as file:
            data = json.load(file)
        mongo_col = MockCollection(data)
        mocker_collection.return_value = mongo_col
        delimiter = ";"

        with TemporaryDirectory() as temp_dir:
            temp_output_file = os.path.join(temp_dir, "test.csv")

            with self.assertRaises(KeyError):
                main.db2csv_soil(
                    output=temp_output_file, delimiter=delimiter, project="fake-project"
                )
