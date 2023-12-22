import json
import re
import uuid
import argparse

import pandas as pd

inventory_template = {
    "_id": None,
    "Date": None,
    "Authors": [],
    "Group": "Flora",
    "Project": None,
    "Community": None,
    "Community_Authors": [],
    "Community_Year": None,
    "Subcommunity": None,
    "Subcommunity_Authors": [],
    "Subcommunity_Year": None,
    "Location": None,
    "MGRS": None,
    "Natural_Site": None,
    "Lithology": None,
    "Coverage": None,
    "Altitude": None,
    "Plot_Slope": None,
    "Alt_Veg": None,
    "Plot_Area": None,
    "Plot_Orientation": None,
    "Ecology": None,
    "Species": [],
    "Pictures": [],
    "DataOrigin":"XLSX"
}

def process_authors(dataframe: pd.DataFrame, row_index: int, column_name: str) -> list[str]:
    """
    Processes the authors from a given dataframe column and returns a list of unique authors.
    
    Args:
        dataframe (pd.DataFrame): The dataframe containing the data.
        row_index (int): The index of the row in the dataframe.
        column_name (str): The name of the column in the dataframe.
    
    Returns:
        List[str]: A list of unique authors.
    """
    
    # Define a list of words to delete from the authors list
    words_to_delete = ["al.", "col.", "cols.", ""]
    
    # Define a pattern to split the column value
    pattern = re.compile(r"; | & |, | ,| et | y | ex | em. | corr. |in ")
    
    # Split the column value based on the pattern
    authors = re.split(pattern, str(dataframe.iloc[row_index][column_name]))
    
    # Remove leading and trailing spaces from each author and filter out certain words
    authors = [author.strip() for author in authors if author.strip() not in words_to_delete]
    
    # Get the unique authors by converting the authors list to a set and then back to a list
    unique_authors = list(set(authors))
    
    # Return the list of unique authors
    return unique_authors


def append_to_dict(object_dict: dict, 
                   object_dict_key: str, 
                   dataframe: pd.DataFrame, 
                   dataframe_row: int, 
                   dataframe_column: str, 
                   type: str, 
                   mgrs_zone: str) -> dict:
    """
    Appends a value to a dictionary based on the specified key and data type.
    
    Args:
        object_dict (dict): The dictionary to append the value to.
        object_dict_key (str): The key to use for the value in the dictionary.
        dataframe (pd.DataFrame): The dataframe containing the value.
        dataframe_row (int): The row index of the value in the dataframe.
        dataframe_column (str): The column name of the value in the dataframe.
        type (str): The data type of the value.
        mgrs_zone (str): The MGRS zone to use for the value (only applicable if object_dict_key is "MGRS").
    
    Returns:
        dict: The updated dictionary.
    """
    # List of possible null characters
    possible_null_characters = ["", "-"]
    
    # Get the value from the dataframe
    data_value = dataframe.iloc[dataframe_row][dataframe_column]
    
    # If the value in the dataframe is a null character or an empty list, return the object_dict unchanged
    if data_value in possible_null_characters or (isinstance(data_value, list) and not data_value):
        return object_dict
    
    # Append the value to the object_dict based on the data type and object_dict_key
    if type == "str":
        if object_dict_key == "MGRS":
            # If object_dict_key is "MGRS", append the value with the MGRS zone
            mgrs = mgrs_zone + str(data_value).replace(" ", "") if mgrs_zone not in str(data_value) else str(data_value).replace(" ", "")
            object_dict[object_dict_key] = mgrs
        else:
            # If object_dict_key is not "MGRS", append the value as a string with leading and trailing whitespaces stripped
            object_dict[object_dict_key] = str(data_value).strip()
    elif type == "int":
        # Append the value as an integer
        object_dict[object_dict_key] = int(data_value)
    elif type == "float":
        # Append the value as a float
        object_dict[object_dict_key] = float(data_value)
    elif type == "list" and object_dict_key in ["Community_Authors", "Subcommunity_Authors"]:
        # If object_dict_key is "Community_Authors" or "Subcommunity_Authors", process the authors and append the resulting array
        authors_array = process_authors(dataframe, dataframe_row, dataframe_column)
        object_dict[object_dict_key] = authors_array
    
    return object_dict


def index_transformation(index):
    """
    Transforms the given index according to a set of predefined transformations.

    Args:
        index (int or float): The index to be transformed.

    Returns:
        str: The transformed index.

    """
    # Define the transformations
    transformations = {
        "(+)": "+",
        "+.2": "+",
        ".": "-",
        "x": "-",
        "X": "-",
        "r": "+"
    }

    # Convert float index to int if necessary
    if isinstance(index, float):
        index = int(index)

    # Convert index to string and apply transformation
    index = str(index)
    return transformations.get(index, index)[0]


def process_species(dataframe: pd.DataFrame, column: str, position: int) -> tuple[list[dict[str, str]], int]:
    """
    Process the species data in the given dataframe and returns a list of species
    along with the current position in the dataframe.

    Args:
        dataframe: The dataframe containing the species data.
        column: The column name containing the species information.

    Returns:
        A tuple containing:
        - A list of dictionaries representing the species.
        - The current position in the dataframe.
    """
    # Initialize an empty list to store the species
    species_list = []

    # Process the species data until an empty value is encountered
    while position < len(dataframe) and dataframe.iloc[position][column] != "":
        # Transform the index value
        index = index_transformation(dataframe.iloc[position][column])

        # If the index is not "-", add the species to the list
        if index != "-":
            species = {
                "Name": str(dataframe.iloc[position].iloc[0]).strip(),
                "Ind": index,
            }
            species_list.append(species)

        # Move to the next position
        position += 1

    # Return the list of species and the current position
    return species_list, position


def main(
    filepath: str,
    natural_site: str,
    mgrs_zone: str,
    output: str,
):
    """
    Reads data from an Excel file, processes it, and generates a JSON file.

    Args:
        filepath (str): The path to the Excel file.
        natural_site (str): The natural site identifier.
        mgrs_zone (str): The MGRS zone identifier.
        output (str): The path to the output JSON file.
    """
    # Create a template for the inventory
    inventory = inventory_template
    # Create an empty list to store the JSON objects
    json_list_to_return = []

    # Read the data from the Excel file
    data = pd.read_excel(filepath, header=None)
    # Remove empty columns and fill NaN values with empty strings
    data = data.dropna(axis=1, how="all").fillna("")

    # Set the natural site value in the inventory
    inventory["Natural_Site"] = natural_site
    # Process each column in the data
    for col in data.columns:
        # Generate a unique ID for the inventory item
        inventory["_id"] = str(uuid.uuid1())
        
        # If the column index is 0, process the community/subcommunity data
        if col == 0:
            # Define the keys and their corresponding column indexes and data types
            keys = [
                ("Community", 0, "str"),
                ("Community_Authors", 1, "list"),
                ("Community_Year", 2, "int"),
                ("Subcommunity", 3, "str"),
                ("Subcommunity_Authors", 4, "list"),
                ("Subcommunity_Year", 5, "int"),
            ]
            # Append the data to the inventory dictionary
            for key, column, data_type in keys:
                inventory = append_to_dict(
                    inventory, key, data, column, col, data_type, mgrs_zone
                )
        else:
            # Process the species data for the current column
            species, final_position = process_species(data, col, 15)
            
            # Create a copy of the inventory for the current column
            inventory_to_return = inventory.copy()
            # Set the species value in the inventory
            inventory_to_return["Species"] = species
            
            # Define the keys and their corresponding column indexes and data types
            keys = [
                ("Plot_Orientation", 7, "str"),
                ("Plot_Slope", 8, "float"),
                ("Altitude", 9, "float"),
                ("Coverage", 10, "float"),
                ("Plot_Area", 11, "float"),
                ("Lithology", 12, "str"),
                ("Alt_Veg", 13, "float"),
                ("Location", final_position + 1, "str"),
                ("MGRS", final_position + 2, "str"),
                
            ]
            
            # Append the data to the inventory dictionary
            for key, column, data_type in keys:
                inventory_to_return = append_to_dict(
                    inventory_to_return, key, data, column, col, data_type, mgrs_zone
                )

            # Add the inventory object to the list
            json_list_to_return.append(inventory_to_return)

    # Write the JSON list to the output file
    with open(output, "w", encoding="utf8") as outfile:
        json.dump(json_list_to_return, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transforms XLSX file with flora inventory data into a JSON file.")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath of the xlsx file",
    )

    parser.add_argument(
        "--natural-site",
        type=str,
        required=True,
        help="Name of the Natural Site associated to the inventory",
    )

    parser.add_argument(
        "--mgrs-zone",
        type=str,
        default="30S",
        help="MGRS grid with the zone number followed by the zone letter",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared] The path to save the generated cluster map image",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()
    
    main(
        args.filepath,
        args.natural_site,
        args.mgrs_zone,
        args.output +"/output.json",
    )
