import argparse
import copy
import json
import re
from typing import Any, Dict, List, Tuple

import docx
from docx import Document

INVENTORY_TEMPLATE = {
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
    "DataOrigin" : "WORD"
}


def extract_data(
    doc: Document,
) -> Tuple[List[List[str]], List[List[str]], List[List[str]], List[List[str]], int]:
    """
    Extracts relevant data from the document.

    Args:
        doc (Document): The document to extract data from.

    Returns:
        Tuple[List[List[str]], List[List[str]], List[List[str]], List[List[str]], int]: A tuple containing the extracted data in the following order:
            - initial_list: The initial list.
            - argument_list: The argument list.
            - species_list: The species list.
            - locality_list: The locality list.
            - num_inventarios: The number of inventarios.
    """
    # Extract the text from each paragraph
    paragraph_texts = [paragraph.text for paragraph in doc.paragraphs]

    # Split the text by tab character
    split_paragraphs = [
        paragraph_text.split("\t") for paragraph_text in paragraph_texts
    ]

    # Split the complete list into initial, argument, and species lists
    initial_list = split_paragraphs[:3]
    split_paragraphs = (
        split_paragraphs[5:] if "" not in split_paragraphs[3] else split_paragraphs[4:]
    )
    argument_list = split_paragraphs[:7]

    # Check if the argument list contains additional arguments
    if "" not in split_paragraphs[7]:
        argument_list.append(split_paragraphs[7])
        split_paragraphs = split_paragraphs[8:]
    else:
        split_paragraphs = split_paragraphs[7:]

    # Find the index of the "localidad" element and get the following elements
    locality_list = split_paragraphs[
        next(
            i
            for i, item in enumerate(split_paragraphs)
            if "localidad" in item[0].lower()
        )
        + 1 :
    ]

    # Remove the "localidad" elements from the complete list
    split_paragraphs = [
        element for element in split_paragraphs if element not in locality_list
    ]

    # Filter out empty or single-element lists from the complete list
    species_list = [
        element
        for element in split_paragraphs
        if "" not in element and len(element) != 1
    ]

    # Count the number of inventarios in the document
    num_inventarios = sum(
        [
            1
            for paragraph_text in paragraph_texts
            if "inventario" in paragraph_text.lower()
            for word in paragraph_text.split()
            if word.isdigit()
        ]
    )

    return (initial_list, argument_list, species_list, locality_list, num_inventarios)


def ind_transform(index: str) -> str:
    """
    Transform the given index based on predefined rules.

    Args:
        index: The index to be transformed.

    Returns:
        The transformed index.
    """
    # Define the transformations dictionary
    transformations = {"(+)": "+", "+.2": "+", ".": "-", "x": "-", "X": "-", "r": "+"}

    # Return the transformed index
    return transformations.get(index, index[0] if len(index) == 3 else index)


def fill_json(
    json_set: List[Dict[str, Any]],
    natural_site: str,
    initial_list: List[List[str]],
    argument_list: List[List[str]],
    species_list: List[List[str]],
    location_list: List[List[str]],
    num_inventories: int,
) -> List[Dict[str, Any]]:
    """
    Fill the json_set list with information from various sources.

    Args:
        json_set: A list of dictionaries representing JSON objects.
        natural_site: The natural site associated with the data.
        initial_list: A list of lists containing initial data.
        argument_list: A list of lists containing argument data.
        species_list: A list of lists containing species data.
        location_list: A list of lists containing location data.
        num_inventories: The number of inventories to process.

    Returns:
        A list of dictionaries representing the updated json_set.
    """
    # Define the list of arguments and their equivalents
    argument_equivalents = {
        "inventario": "_id",
        "orientación": "Plot_Orientation",
        "inclinación": "Plot_Slope",
        "altitud": "Altitude",
        "cobertura": "Coverage",
        "área": "Plot_Area",
        "litología": "Lithology",
        "altura": "Alt_Veg",
    }

    # Create a dictionary of arguments and their corresponding values
    arguments = {
        argument: element[1:]
        for argument in argument_equivalents.keys()
        for element in argument_list
        if argument in element[0].lower()
    }

    # Populate the json_set list with species information
    for inventory, index in zip(json_set, range(num_inventories)):
        inventory["Species"] = [
            {"Name": species[0], "Ind": ind_transform(species[index + 1])}
            for species in species_list
        ]

    # Extract the authors from the document
    authors = initial_list[1][0].split(" in ")[1]
    authors_list = re.split(", |& ", authors)
    authors = [author.strip() for author in authors_list]

    # Populate the json_set list with inventory information
    for index in range(num_inventories):
        json_set[index]["Community"] = initial_list[0][0]
        json_set[index]["Authors"] = authors
        json_set[index]["Community_Year"] = int(initial_list[2][0].split()[0])
        location = re.split(", | MGRS: ", location_list[index][0])
        json_set[index]["Location"] = location[1]
        if len(location) == 3:
            mgrs = location[2].replace(" ", "").replace(".", "")
            json_set[index]["MGRS"] = "30S" + mgrs if "30S" not in mgrs else mgrs

    # Assign argument values to the json_set dictionary
    for index, item in enumerate(json_set[:num_inventories]):
        for argument in argument_equivalents:
            if argument in arguments:
                arg_label = argument_equivalents[argument]
                item[arg_label] = arguments[argument][index]

    # Add community and natural site information to the json_set dictionary
    for element in json_set:
        if element["Community"] != "":
            element["_id"] = (
                element["_id"] + "-" + element["Community"].replace(" ", "_")
            )
        element["Natural_Site"] = natural_site

    return json_set


def main(
    filepath: str,
    natural_site: str,
    output: str,
) -> None:
    """
    Refactored version of the main function.
    Args:
        filepath (str): Path to the input document file.
        natural_site (str): Name of the natural site.
        output (str): Path to the output JSON file.
    Returns:
        None: The function does not return any value.
    """

    # Open the document file
    doc = docx.Document(filepath)

    # Extract inventory data and store them in lists to improve access to them
    (
        initial_list,
        argument_list,
        species_list,
        locality_list,
        num_inventarios,
    ) = extract_data(doc)

    # Create a list of inventory templates
    json_set = [copy.deepcopy(INVENTORY_TEMPLATE) for _ in range(num_inventarios)]

    # Fill json
    json_set = fill_json(
        json_set,
        natural_site,
        initial_list,
        argument_list,
        species_list,
        locality_list,
        num_inventarios,
    )

    # Write the json_set dictionary to the output JSON file
    with open(output, "w", encoding="utf-8") as file:
        file.write(json.dumps(json_set, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Word to Flora JSON")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Name of the Word file",
    )

    parser.add_argument(
        "--natural-site",
        type=str,
        required=True,
        help="Name of the Natural Site",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    main(
        args.filepath,
        args.natural_site,
        args.output+"/output.json",
    )
