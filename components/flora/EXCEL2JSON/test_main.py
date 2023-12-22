import unittest
import tempfile
from main import *

class EXCEL2JSONTestCase(unittest.TestCase):
    
    def setUp(self):
        # Create a sample dataframe for testing
        self.dataframe = pd.DataFrame({
            "Author": ["John Doe; Jane Smith", "John Doe, Jane Smith", "John Doe & Jane Smith", "John Doe, Jane Smith et al."],
        })
    
    def test_process_authors(self):
        # Test case where authors are separated by semicolon
        expected_result = ["John Doe", "Jane Smith"]
        result = process_authors(self.dataframe, 0, "Author")
        self.assertCountEqual(result, expected_result)
        
        # Test case where authors are separated by comma
        expected_result = ["John Doe", "Jane Smith"]
        result = process_authors(self.dataframe, 1, "Author")
        self.assertCountEqual(result, expected_result)
        
        # Test case where authors are separated by ampersand
        expected_result = ["John Doe", "Jane Smith"]
        result = process_authors(self.dataframe, 2, "Author")
        self.assertCountEqual(result, expected_result)
        
        # Test case where authors contain words to delete
        expected_result = ["John Doe", "Jane Smith"]
        result = process_authors(self.dataframe, 3, "Author")
        self.assertCountEqual(result, expected_result)
        
    def test_append_to_dict(self):
        object_dict = {}
        dataframe = pd.DataFrame({"Column": ["Value"]})
        object_dict = append_to_dict(object_dict, "Key", dataframe, 0, "Column", "str", "")
        self.assertEqual(object_dict["Key"], "Value")

        object_dict = {}
        dataframe = pd.DataFrame({"Column": [1]})
        object_dict = append_to_dict(object_dict, "Key", dataframe, 0, "Column", "int", "")
        self.assertEqual(object_dict["Key"], 1)
        
        object_dict = {}
        dataframe = pd.DataFrame({"Column": [1.5]})
        object_dict = append_to_dict(object_dict, "Key", dataframe, 0, "Column", "float", "")
        self.assertEqual(object_dict["Key"], 1.5)

        object_dict = {"Key": "Value"}
        dataframe = pd.DataFrame({"Column": [""]})
        object_dict = append_to_dict(object_dict, "Key", dataframe, 0, "Column", "str", "")
        self.assertEqual(object_dict["Key"], "Value")

        object_dict = {"Key": "Value"}
        dataframe = pd.DataFrame({"Column": [[]]})
        object_dict = append_to_dict(object_dict, "Key", dataframe, 0, "Column", "str", "")
        self.assertEqual(object_dict["Key"], "Value")
        
    def test_index_transformation(self):
        self.assertEqual(index_transformation(1), "1")
        self.assertEqual(index_transformation(1.2), "1")
        self.assertEqual(index_transformation("."), "-")
        self.assertEqual(index_transformation("x"), "-")
        self.assertEqual(index_transformation("X"), "-")
        self.assertEqual(index_transformation("r"), "+")

    def test_process_species(self):
        # Create a sample dataframe for testing
        data = {
            "Species": ["Species 1", "Species 2", "Species 3"],
            "Column1": ["+", "-", "+"]
        }
        df = pd.DataFrame(data)

        # Call the process_species function
        species_list, position = process_species(df, "Column1", 0)

        # Define the expected result
        expected_species_list = [
            {"Name": "Species 1", "Ind": "+"},
            {"Name": "Species 3", "Ind": "+"}
        ]
        expected_position = 3

        # Assert that the returned species list and position match the expected result
        self.assertEqual(species_list, expected_species_list)
        self.assertEqual(position, expected_position)
        
    def test_main(self):
        # Create temporary files with .xlsx and .json extensions
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_excel, \
                tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_json:
            
            # Get the file path of the temporary excel file
            filepath = temp_excel.name
            
            # Create a DataFrame with the given data
            df = pd.DataFrame({
                0: ["Metadata - 1", "Metadata - 2", 2023, "Metadata - 4", "", "", "INVENTARIO Nº", "Orientación", 
                    "Inclinación (º)", "Altitud (m)", "Cobertura (%)", "Área (m 2)", "Litología", "Altura vegetación (cm)", 
                    "", "Species1", "Species2", "Species3", "", "Localidad", "UTM"],
                1: ["", "", "", "", "", "", 1, "S", 30, 0, 80, 4, "Lit-1", 2, "", "+", "+", "+", "", "Loc-1", "Utm-1"],
                2: ["", "", "", "", "", "", 2, "N", 50, 4, 20, 6, "Lit-2", 0, "", "+", "-", "+", "", "Loc-2", "Utm-2"]
            })
            
            # Save the DataFrame as an excel file
            df.to_excel(filepath, index=False, header=False)

            # Define the values for natural_site, mgrs_zone, and output
            natural_site = "Site A"
            mgrs_zone = "ABC123"
            output = temp_json.name

            # Call the main function with the given parameters
            main(filepath, natural_site, mgrs_zone, output)

            # Open the output file and load its content as JSON
            with open(output) as f:
                data = json.load(f)

            # Assert that the length of the data is 2
            assert len(data) == 2


        
if __name__ == '__main__':
    unittest.main()
