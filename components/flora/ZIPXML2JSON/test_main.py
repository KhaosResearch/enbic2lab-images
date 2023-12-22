import unittest
from unittest.mock import MagicMock

from untangle import Element

from main import (LABEL_MAPPING, extract_community_info, extract_features_data,
                  extract_species, index_transform, update_authors)


class IndexTransformTestCase(unittest.TestCase):
    def test_index_transform(self):
        # Test cases for positive index
        assert index_transform("(+)") == "+"
        assert index_transform("+.2") == "+"

        # Test cases for negative index
        assert index_transform(".") == "-"
        assert index_transform("x") == "-"
        assert index_transform("X") == "-"

        # Test cases for positive alphabetic index
        assert index_transform("r") == "+"
        assert index_transform("abc") == "a"

        # Test cases for positive numeric index
        assert index_transform("123") == "1"

    def test_update_authors(self):
        # Define a list of test cases with different inputs and expected outputs
        test_cases = [
            {
                "new_authors": "John Doe; Jessica Hart",
                "old_authors": ["John Doe", "Jane Smith"],
                "not_equal": [],
                "not_allowed": [],
                "extra_strip": False,
                "expected_result": ["John Doe", "Jane Smith", "Jessica Hart"],
            },
            {
                "new_authors": " John Doe, Jessica Hart   ",
                "old_authors": ["John Doe", "Jane Smith"],
                "not_equal": [],
                "not_allowed": [],
                "extra_strip": True,
                "expected_result": ["John Doe", "Jane Smith", "Jessica Hart"],
            },
            {
                "new_authors": "John Doe; Jessica Hart",
                "old_authors": ["John Doe", "Jane Smith"],
                "not_equal": ["Jessica Hart"],
                "not_allowed": [],
                "extra_strip": False,
                "expected_result": ["John Doe", "Jane Smith"],
            },
            {
                "new_authors": "John Doe; Jessica Hart",
                "old_authors": ["John Doe", "Jane Smith"],
                "not_equal": [],
                "not_allowed": ["Hart"],
                "extra_strip": False,
                "expected_result": ["John Doe", "Jane Smith"],
            },
        ]

        # Iterate through each test case and verify the result
        for test_case in test_cases:
            # Call the update_authors function with the test case inputs
            result = update_authors(
                test_case["new_authors"],
                test_case["old_authors"],
                test_case["not_equal"],
                test_case["not_allowed"],
                test_case["extra_strip"],
            )
            # Verify that the result matches the expected result
            self.assertEqual(result, test_case["expected_result"])

    def test_extract_community_info(self):
        # Create a mock object for rel
        rel = MagicMock()

        # Set the cdata attribute of rel.OriginalSyntaxonName
        rel.OriginalSyntaxonName.cdata = "Rusco hypophylli-Quercetum canariensis Rivas Goday; Rivas Mart. ex Rivas Mart. 1974 subass. quercetosum broteroi Pérez Latorre; Cabezudo in Pérez Latorre; al. 1996"

        # Create an empty dictionary to store the JSON data
        json_dict = {"Community_Authors": [], "Subcommunity_Authors": []}

        # Set the separator string
        sep = " "

        # Define the expected output dictionary
        expected_output = {
            "Community_Authors": ["Rivas Goday", "Rivas Mart."],
            "Subcommunity_Authors": ["Pérez Latorre", "Cabezudo"],
            "Community_Year": 1974,
            "Community": "Rusco hypophylli-Quercetum canariensis",
            "Subcommunity": "quercetosum broteroi",
            "Subcommunity_Year": 1996,
        }

        # Call the extract_community_info function with the provided inputs
        output = extract_community_info(rel, json_dict, sep)

        # Assert that the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_extract_features_data(self):
        # Define the input values
        values = ["Test Locµti®ÿon", "10", "55", "North", "100", "35", "SIVIM"]

        # Create a list to store the datums
        datums = []

        # Iterate over the LABEL_MAPPING and create datums
        for i, label in enumerate(LABEL_MAPPING):
            # Create a new Datum element
            datum = Element("Datum", {"label": label})

            # Create a new value element
            value = Element("value", {})

            # Add the value data as CDATA
            value.add_cdata(values[i])

            # Add the value element as a child of datum
            datum.add_child(value)

            # Append the datum to the datums list
            datums.append(datum)

        # Create a MagicMock object with the datums
        rel = MagicMock(SideData=[MagicMock(Datum=datums)])

        # Create an empty dictionary to store the JSON data
        json_dict = {}

        # Set the index value
        index = 0

        # Define the expected output
        expected_output = {
            "Alt_Veg": 35.0,
            "Altitude": 10.0,
            "Coverage": 100.0,
            "Location": "Test Location",
            "Plot_Orientation": "North",
            "Plot_Slope": 55.0,
            "DataOrigin": "SIVIM"
        }

        # Call the extract_features_data function and store the output
        output = extract_features_data(rel, json_dict, index)

        # Assert that the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_extract_species(self):
        # Create a mock object for 'rel'
        rel = MagicMock()

        # Set the 'ReleveEntry' attribute of the mock object to a list of dictionaries
        rel.ReleveEntry = [
            {
                "accepted_name": "Species 1 subsp. Subspecies bad data",
                "original_name": "Original 1",
                "value": "+",
            },
            {
                "accepted_name": None,
                "original_name": "Original 2 var. VarOriginal bad data",
                "value": "-",
            },
        ]

        # Create an empty dictionary 'json_dict'
        json_dict = {"Species": []}

        # Set the separator string to ' '
        sep = " "

        # Define the expected output dictionary
        expected_output = {
            "Species": [
                {"Name": "Species 1 subsp. Subspecies", "Ind": "+"},
                {"Name": "Original 2 var. VarOriginal", "Ind": "-"},
            ]
        }

        # Call the 'extract_species' function with the mock object and input data
        output = extract_species(rel, json_dict, sep)

        # Assert that the output matches the expected output
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
