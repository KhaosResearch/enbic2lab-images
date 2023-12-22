import os
import re
import pandas as pd
import unittest
from main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        # Create a test CSV file with the same data as the example file
        data = {
            "support": [0.012, 0.024, 0.048],
            "itemsets": ["Node1, Node2", "Node3, Node2", "Node4, Node2"],
        }
        self.test_data = pd.DataFrame(data)
        self.test_data.to_csv("test_data.csv", index=False, sep=";")

    def tearDown(self):
        # Delete test files
        os.remove("test_data.csv")
        os.remove("test_output.html")

    def test_main(self):
        # Run the script with the test CSV file and verify that the output HTML file is generated
        main("test_data.csv", ";", "test_output.html")

        # Verify that the output HTML file was generated correctly
        self.assertTrue(os.path.exists("test_output.html"))

        # Verify that the expected edges have been generated
        expected_edges = [
            ("Node1", "Node2", 0.012),
            ("Node3", "Node2", 0.024),
            ("Node4", "Node2", 0.048),
        ]
        with open("test_output.html", "r") as f:
            html = f.read()

        patron = r"edges = new vis\.DataSet\((.*?)\);"

        edge_html = re.findall(patron, html)

        for edge in expected_edges:
            self.assertIn(
                f'{{"from": "{edge[0]}", "title": "Fidelity = {(round(edge[2]*100,2))}%", "to": "{edge[1]}", "value": {edge[2]*2}}}',
                edge_html[0],
            )


if __name__ == "__main__":
    unittest.main()
