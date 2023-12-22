import argparse
import copy
import json
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

import untangle
from untangle import Element

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
    "DataOrigin":"SIVIM"
}

LABEL_MAPPING = {
    "Locality": "Location",
    "Altitude": "Altitude",
    "Inclination": "Plot_Slope",
    "Aspect": "Plot_Orientation",
    "Total Cover (%)": "Coverage",
    "Shrub Height (m)": "Alt_Veg",
    "DataOrigin":"DataOrigin"
}

SPECIAL_CHARACTER_REPLACEMENTS = {
    "¡": "í",
    "\u00a6": ".",
    "¢": "ó",
    "\u00a0": "a",
    "\u00a3": "u",
    "¤": "ñ",
    "®ÿ": "",
    "µ": "a",
}


def index_transform(index: str) -> str:
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


def update_authors(
    new_authors: str,
    old_authors: List[str],
    not_equal: List[str],
    not_allowed: List[str],
    extra_strip: bool,
) -> List[str]:
    """
    Update the list of authors with new authors, following certain rules.

    Args:
        new_authors (str): A string containing the new authors.
        old_authors (List[str]): A list of old authors.
        not_equal (List[str]): A list of authors that should not be added.
        not_allowed (List[str]): A list of words that should not be present in the authors.
        extra_strip (bool): A boolean indicating whether to apply extra stripping.

    Returns:
        List[str]: The updated list of authors.
    """

    # Create a copy of the old authors list
    updated_authors = old_authors.copy()

    # Split the new_authors string using multiple delimiters
    new_authors_list = re.split(
        r"; | & |, | ,| et | y | ex | em. | corr. |in ",
        new_authors,
    )

    # Iterate over each author in the new_authors_list
    for author in new_authors_list:
        # Apply extra stripping if required
        auth_updated = author.strip().strip(",") if extra_strip else author.strip()

        # Check if the author meets all the conditions to be added to the updated_authors list
        if (
            auth_updated not in updated_authors
            and not str.isdigit(auth_updated)
            and auth_updated not in not_equal
            and not any(word in auth_updated for word in not_allowed)
        ):
            # Add the author to the updated_authors list
            updated_authors.append(auth_updated)

    return updated_authors


def extract_community_info(
    rel: Element, json_dict: Dict[str, Any], sep: str
) -> Dict[str, Any]:
    """
    Extracts information about a community from a given relationship object.

    Args:
        rel (Element): The relationship object.
        json_dict (Dict[str, Any]): The dictionary to store the extracted information.
        sep (str): The separator character to use.

    Returns:
        Dict[str, Any]: The updated dictionary with the extracted information.
    """
    # Split the original syntaxon name by " subass. "
    interest_community = rel.OriginalSyntaxonName.cdata.split(" subass. ")

    # Split the community name by spaces
    community = interest_community[0].split()

    # Establish by default not found
    found = False

    # Loop through the community name
    for index, word in enumerate(community):
        # Check if the word ends with specific suffixes
        if not found and word.endswith(
            (
                "etea",
                "etalia",
                "enalia",
                "ion",
                "enion",
                "etum",
                "etosum",
            )
        ):
            found = True
            word_index = index + 1

            # Handle special case where "etum" is part of the word
            if community[word_index] != "in" and "etum" in word:
                word_index += 1

            # Extract the community and author names
            com = sep.join(community[:word_index]).strip()
            aut = sep.join(community[word_index:-1]).strip()

            # Split authors by " nom."
            list_authors = aut.split(" nom.")
            if len(list_authors) > 1:
                # Extract author names and check for year
                for i, author in enumerate(list_authors[:2]):
                    list_date = author.split()
                    if str.isdigit(list_date[-1]):
                        json_dict["Community_Year"] = int(list_date[-1])
                        list_authors[i] = sep.join(list_date[:-1])
                        break

            # Update the "Community_Authors" value in json_dict
            new_authors = sep.join(list_authors).replace("(", ",").replace(")", ",")
            json_dict["Community_Authors"] = update_authors(
                new_authors,
                json_dict["Community_Authors"],
                ["al.", ""],
                ["col.", "cols."],
                True,
            )

    if not found:
        if community[0] == "Comunidad":
            not_equal = ["al.", "", "*"]
            if len(community) > 4 and community[4] == "y":
                num = 9 if community[7] == "subsp." else 7
            elif len(community) > 4 and community[4] == "subsp.":
                num = 6
            else:
                not_equal.remove("*")
                num = 4

            # Extract community name
            com = sep.join(community[0:num]).strip()
            # Extract author names
            new_authors = sep.join(community[num:-1])
            # Update the "Community_Authors" value in json_dict
            json_dict["Community_Authors"] = update_authors(
                new_authors,
                json_dict["Community_Authors"],
                not_equal,
                ["col.", "cols."],
                False,
            )

            if str.isdigit(community[-1]):
                json_dict["Community_Year"] = int(community[-1])
        else:
            # Extract community name
            com = (
                sep.join(community[:-1]).strip()
                if str.isdigit(community[-1]) or community[-1] == "**"
                else sep.join(community).strip()
            )
    else:
        if str.isdigit(community[-1]):
            json_dict["Community_Year"] = int(community[-1])
    json_dict["Community"] = com

    if len(interest_community) > 1:
        subcommunity = interest_community[1].split()
        json_dict["Subcommunity"] = sep.join(subcommunity[0:2]).strip()

        if len(subcommunity) > 2 and subcommunity[2] != "*":
            # Extract subcommunity author names
            list_subcom_aut = (
                subcommunity[2:-1]
                if str.isdigit(subcommunity[-1])
                else subcommunity[2:]
            )
            new_authors = (
                sep.join(list_subcom_aut).strip().replace("(", ",").replace(")", ",")
            )

            # Update the "Subcommunity_Authors" value in json_dict
            json_dict["Subcommunity_Authors"] = update_authors(
                new_authors,
                json_dict["Subcommunity_Authors"],
                [""],
                ["col.", "cols.", "al."],
                True,
            )

        if str.isdigit(subcommunity[-1]):
            json_dict["Subcommunity_Year"] = int(subcommunity[-1])
    return json_dict


def extract_features_data(
    rel: Element, json_dict: Dict[str, Any], index: int
) -> Dict[str, Any]:
    """
    Extracts features data from a given Element and updates a JSON dictionary.

    Args:
        rel (Element): The Element instance containing the data.
        json_dict (Dict[str, Any]): The JSON dictionary to update.
        index (int): The index of the element in the rel list.

    Returns:
        Dict[str, Any]: The updated JSON dictionary.
    """
    # Iterate through the SideData elements
    for sd in rel.SideData[index].Datum:
        # Get the label of the SideData element
        label = sd["label"]

        # Check if the label is in the label mapping
        if label in LABEL_MAPPING:
            # Map the label to a key using LABEL_MAPPING, if available
            key = LABEL_MAPPING.get(label)
            # Get the value of the SideData element
            value = sd.value.cdata

            # If the key is "Location", replace special characters in the value
            if key == "Location" or key == "DataOrigin":
                value = re.sub(
                    "|".join(SPECIAL_CHARACTER_REPLACEMENTS.keys()),
                    lambda m: SPECIAL_CHARACTER_REPLACEMENTS[m.group()],
                    value,
                )
            # If the key is in this list, convert the value to float if possible
            elif key in ["Altitude", "Plot_Slope", "Coverage", "Alt_Veg"]:
                try:
                    value = float(value)
                except ValueError:
                    continue

            # Update the JSON dictionary with the key-value pair
            json_dict[key] = value

    # Return the updated JSON dictionary
    return json_dict


def extract_species(
    rel: Element, json_dict: Dict[str, Any], sep: str
) -> Dict[str, Any]:
    """
    Extracts species information from a given Element object and adds it to a JSON dictionary.

    Args:
        rel (Element): The Element object containing the species information.
        json_dict (Dict[str, Any]): The JSON dictionary to which the species information will be added.
        sep (str): The separator character to use.

    Returns:
        Dict[str, Any]: The updated JSON dictionary.
    """

    for sp in rel.ReleveEntry:
        name = sp["accepted_name"] if sp["accepted_name"] else sp["original_name"]
        specie_array = name.split()

        if "subsp." in name:
            # If the species name contains "subsp.", concatenate the first two words with the next two words
            species_name = (
                sep.join(specie_array[:2])
                + sep
                + sep.join(
                    specie_array[
                        specie_array.index("subsp.") : specie_array.index("subsp.") + 2
                    ]
                )
            )
        elif "var." in name:
            # If the species name contains "var.", concatenate the first two words with the next two words
            species_name = (
                sep.join(specie_array[:2])
                + sep
                + sep.join(
                    specie_array[
                        specie_array.index("var.") : specie_array.index("var.") + 2
                    ]
                )
            )
        else:
            # If the species name does not contain "subsp." or "var.", concatenate only the first two words
            species_name = sep.join(specie_array[:2])

        json_dict["Species"].append(
            {
                "Name": species_name,
                "Ind": index_transform(sp["value"]),
            }
        )

    return json_dict


def readXML(
    xml_file: str, natural_site: str, register_list: List[str]
) -> Tuple[List[dict], List[str]]:
    """
    Read XML file and extract relevant data.

    Args:
        xml_file (str): Path to the XML file.
        natural_site (str): Name of the natural site.
        register_list (List[str]): List of registered names.

    Returns:
        Tuple[List[dict], List[str]]: A tuple containing the extracted data as a list of dictionaries and a list of addressed names.
    """
    sep = " "
    xml_list = []
    names_addressed = []

    # Parse the XML file
    doc = untangle.parse(xml_file)

    # Iterate over each Releve in the ReleveTable
    for rel in doc.ReleveTable.Releve:
        json_dict = copy.deepcopy(INVENTORY_TEMPLATE)

        # Check if the name is not in the register_list
        if rel["name"] not in register_list:
            json_dict["_id"] = rel["name"]
            json_dict["Natural_Site"] = natural_site.replace("_", " ")
            json_dict["Plot_Area"] = float(rel.PlotArea.cdata)
            json_dict["MGRS"] = rel.CitationCoordinate["code"]

            # Extract community info if it exists
            if hasattr(rel, "OriginalSyntaxonName"):
                json_dict = extract_community_info(rel, json_dict, sep)

            # Extract features data from SideData[1] if it exists
            if hasattr(rel.SideData[1], "Datum"):
                json_dict = extract_features_data(rel, json_dict, 1)

            # Extract features data from SideData[2] if it exists
            if hasattr(rel.SideData[2], "Datum"):
                json_dict = extract_features_data(rel, json_dict, 2)

            # Extract species info if it exists
            if hasattr(rel, "ReleveEntry"):
                json_dict = extract_species(rel, json_dict, sep)

            xml_list.append(json_dict)
            names_addressed.append(rel["name"])

    return xml_list, names_addressed


def main(filepath: str, natural_site: str, output: str):
    """
    Extracts XML files from a zip file, processes them, and saves the result as JSON.

    Args:
        filepath (str): Path to the zip file.
        natural_site (str): Natural site name.
        output (str): Path to save the resulting JSON file.
    """

    # Extract the zip file to a temporary folder
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall("tmp_folder")

    json_final = []
    register_list = []

    # Process each XML file in the directory
    for file_path in Path("tmp_folder").glob("**/*.xml"):
        xml_list, names_addressed = readXML(str(file_path), natural_site, register_list)
        json_final.extend(xml_list)
        register_list.extend(names_addressed)

    # Save the resulting JSON to the specified output file
    with open(output, "w", encoding="utf-8") as file:
        json.dump(json_final, file, indent=4, ensure_ascii=False)

    # Remove the temporary folder
    shutil.rmtree("tmp_folder")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transforms a Zip file to a standard flora JSON file."
    )

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Name of the zip file",
    )

    parser.add_argument(
        "--natural-site",
        type=str,
        required=True,
        help="Name of Natural Site",
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
        args.output+"/output.json",
    )
