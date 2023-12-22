import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from main import calculate_community_statistics, calculate_species_community

class CommunityStatisticsTestCase(unittest.TestCase):

    def test_calculate_community_statistics(self):
        # Test case 1
        data = pd.DataFrame({
            "Community": ["A", "A", "A"],
            "Coverage(%)": [80, 90, 70],
            "Altitude(m)": [100, 200, 150],
            "Species": ["S1", "S2", "S3"],
            "S1": [1, 2, 4],
            "S2": [3, 5, 1],
            "S3": [1, 4, 2],
        }).T
        expected_output = pd.DataFrame({
            "Mean Coverage": [80],
            "Mean Coverage Standard Error": [5.773502691896257],
            "Altitude Difference": [100.0],
            "Min_Alt": [100.0],
            "Max_Alt": [200.0],
            "Number of Species": [3]
        }, index=["A"])
        expected_output.index.name = "Community"
        assert_frame_equal(calculate_community_statistics(data), expected_output, check_dtype=False)

        # Test case 2
        data = pd.DataFrame({
            "Community": ["A", "A", "B", "B", "B"],
            "Coverage(%)": [80, 90, 70, 75, 85],
            "Altitude(m)": [100, 200, 150, 180, 160],
            "Species": ["S1", "S2", "S3", "-", "S4"],
            "S1": [1, 2, 4, 2, 4],
            "S2": [3, "-", 1, 2, 4],
            "S3": [1, 4, 2, 2, 4],
            "S4": [1, 2, 4, 5, 1],
        }).T
        expected_output = pd.DataFrame({
            "Mean Coverage": [85, 76.7],
            "Mean Coverage Standard Error": [5.0, 4.409585518440984],
            "Altitude Difference": [100.0, 30.0],
            "Min_Alt": [100, 150],
            "Max_Alt": [200.0, 180.0],
            "Number of Species": [3, 4]
        }, index=["A", "B"])
        expected_output.index.name = "Community"
        assert_frame_equal(calculate_community_statistics(data), expected_output, check_dtype=False)

    def test_calculate_species_community(self):
        # Test case 1
        data = pd.DataFrame({
            "Community": ["A", "B", "C"],
            "Subcommunity": ["X", "Y", "Z"],
            "Species": ["S1", "S2", "S3"],
            "S1": [1, 2, 4],
            "S2": [3, 5, 1],
            "S3": [1, 4, 2],
        }).T
        expected_output = pd.DataFrame({
            "Community": ["A", "A", "A", "B", "B", "B", "C", "C", "C"],
            "Subcommunity": ["X", "X", "X", "Y", "Y", "Y", "Z", "Z", "Z"],
            "Species": ["S1", "S2", "S3", "S1", "S2", "S3", "S1", "S2", "S3"],
            "Number of Appearances": [1, 1, 1, 1, 1, 1, 1, 1, 1]
        })
        assert_frame_equal(calculate_species_community(data), expected_output, check_dtype=False)

        # Test case 2
        data = pd.DataFrame({
            "Community": ["A", "A", "A", "B", "B", "B"],
            "Subcommunity": ["X", "X", "Y", "Y", "Z", "Z"],
            "Species": ["S1", "S2", "S3", "S4", "S5", "S6"],
            "S1": [1, 2, 4, 2, 4, 6],
            "S2": [3, "-", 1, 2, 4, 2],
            "S3": [1, 4, 2, 2, 4, "-"],
            "S4": [1, 2, 4, 5, 1, 3],
        }).T
        expected_output = pd.DataFrame({
            "Community": ["A", "A", "A", "A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "B", "B", "B"],
            "Subcommunity": ["X", "X", "X", "X", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Z", "Z", "Z", "Z"],
            "Species": ["S1", "S2", "S3", "S4", "S1", "S2", "S3", "S4", "S1", "S2", "S3", "S4", "S1", "S2", "S3", "S4"],
            "Number of Appearances": [2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2]
        })
        assert_frame_equal(calculate_species_community(data), expected_output, check_dtype=False)

if __name__ == "__main__":
    unittest.main()