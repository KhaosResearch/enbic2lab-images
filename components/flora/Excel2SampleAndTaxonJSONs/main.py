import argparse

import pandas as pd


def main(filepath: str, output_folder: str) -> None:
    """
    Read an Excel file, extract specific columns, and save them as JSON files.

    Args:
        filepath (str): The path to the Excel file.
        output_folder (str): The path to the folder where the JSON files will be saved.
    """
    # Read the Excel file
    df = pd.read_excel(filepath)

    # Rename some columns
    column_mapping = {
        "NaturalSite": "Natural_Site",
        "decimalLatitude": "Latitude",
        "decimalLongitude": "Longitude",
    }
    df = df.rename(columns=column_mapping)

    # Add taxon rank acronyms
    rank_mapping = {
        "species": "_",
        "subspecies": "subsp.",
        "variety": "var.",
        "hib": "x",
        "form": "f.",
    }
    df["taxonRankAcronym"] = df["taxonRank"].map(rank_mapping).fillna(df["taxonRank"])

    # Add species names
    df["specieName"] = (
        df[["genus", "species", "taxonRankAcronym", "infraspecificEpithet"]]
        .apply(" ".join, axis=1)
        .apply(lambda x: x.rstrip("_ "))
    )

    # Select sample columns from the dataframe
    sample = df[
        [
            "ENBIC2ID",
            "Natural_Site",
            "gbifID",
            "institutionCode",
            "catalogNumber",
            "scientificName",
            "aut_infra",
            "taxonRankInterpreted",
            "speciesInterpreted",
            "identifiedBy",
            "dateIdentified",
            "countryCode",
            "stateProvince",
            "locality",
            "Latitude",
            "Longitude",
            "coordinateUncertaintyInMeters",
            "elevation",
            "recordedBy",
            "eventDate",
            "remarks",
            "MGRS",
            "specieName",
        ]
    ]

    # Save the selected columns as a JSON file
    sample.to_json(
        f"{output_folder}/sample.json", orient="records", indent=2, force_ascii=False
    )

    # Select taxon columns from the dataframe
    taxon = df[
        [
            "genus",
            "species",
            "taxonRank",
            "taxonRankAcronym",
            "infraspecificEpithet",
            "kingdom",
            "phylum",
            "order",
            "class",
            "family",
            "aut_esp",
            "specieName",
        ]
    ].drop_duplicates()

    # Save the selected columns as a JSON file
    taxon.to_json(
        f"{output_folder}/taxon.json", orient="records", indent=2, force_ascii=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates community statistics and species community"
    )
    parser.add_argument(
        "--filepath",
        type=str,
        help="Input XLSX file path.",
    )
    parser.add_argument(
        "--output-folder", type=str, help="Output folder path.", default="/mnt/shared"
    )
    args = parser.parse_args()

    main(
        args.filepath,
        args.output_folder,
    )
