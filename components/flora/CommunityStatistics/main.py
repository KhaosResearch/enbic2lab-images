import argparse
import math

import numpy as np
import pandas as pd


def calculate_community_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate statistics for each community in the given data.

    Args:
    - data: Pandas DataFrame containing the community data.

    Returns:
    - df_final: Pandas DataFrame containing the calculated statistics.
    """

    # Get unique community values
    communities = data.loc["Community"].dropna().unique()
    
    # Create an empty DataFrame to store the statistics
    df_final = pd.DataFrame(
        index=communities,
        columns=[
            "Mean Coverage",
            "Mean Coverage Standard Error",
            "Altitude Difference",
            "Min_Alt",
            "Max_Alt",
            "Number of Species",
        ]
    )

    # Iterate over each community
    for community in communities:
        n_com = 0
        total_cov = 0
        total = []
        max_alt = 0
        min_alt = np.inf

        # Iterate over each column in the data
        for column in data.columns:
            # Check if the community matches the value in the "Community" column
            if community == data.loc["Community", column]:
                n_com += 1

                # Calculate mean coverage
                coverage = float(data.loc["Coverage(%)", column])
                if not math.isnan(coverage):
                    total_cov += coverage
                    total.append(coverage)
                    df_final.loc[community, "Mean Coverage"] = round(
                        total_cov / n_com, 1
                    )

                # Calculate min and max altitude
                altitude = float(data.loc["Altitude(m)", column])
                if not math.isnan(altitude):
                    max_alt = max(max_alt, round(altitude, 1))
                    min_alt = min(min_alt, round(altitude, 1))

                # Update the statistics in the DataFrame
                df_final.loc[community, "Min_Alt"] = min_alt
                df_final.loc[community, "Max_Alt"] = max_alt
                df_final.loc[community, "Altitude Difference"] = max_alt - min_alt
                df_final.index.name = "Community"

                # Calculate the total number of species
                species_index = list(data.index).index("Species")
                total_species = 0
                for i in range(species_index + 1, len(data)):
                    if data.iloc[i][column] != "-":
                        total_species += 1
                df_final.loc[community, "Number of Species"] = total_species

        # Calculate the mean coverage standard error
        data_array = np.array(total)
        mean_coverage_standard_error = np.nanstd(data_array, ddof=1) / np.sqrt(
            np.sum(~np.isnan(data_array))
        )
        df_final.loc[
            community, "Mean Coverage Standard Error"
        ] = mean_coverage_standard_error

    # Remove rows with missing values in the "Mean Coverage" column
    df_final = df_final[df_final["Mean Coverage"].notna()]

    return df_final

def calculate_species_community(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the species community from the given data.

    Args:
        data (pd.DataFrame): The input data containing community and subcommunity information.

    Returns:
        pd.DataFrame: The species community data containing community, subcommunity, species, and number of appearances.

    """

    # Get unique communities from the data
    communities = data.loc["Community"].dropna().unique()

    # Create an empty dataframe to store the species community data
    df_species_com = pd.DataFrame(
        columns=["Community", "Subcommunity", "Species", "Number of Appearances"]
    )

    # Create a list to store the community species information
    community_species = []

    # Loop over each community
    for com in communities:
        # Get the data for the current community
        data_com = data.loc[:, data.loc["Community", :] == com]

        # Create a dictionary to store subcommunity information
        dict_com = {}
        for subcom in data_com.loc["Subcommunity"]:
            if subcom not in dict_com:
                dict_com[subcom] = {}

        # Get the index list of the data
        index_list = list(data_com.index)

        # Loop over each column in the data
        for col in data_com:
            # Get the subcommunity value for the current column
            subcom = data_com.loc["Subcommunity", col]

            # Loop over each row after the "Species" row
            for i in range(index_list.index("Species") + 1, data_com.shape[0]):
                species = data_com.iloc[i][col]
                if species != "-":
                    dict_com[subcom][index_list[i]] = dict_com[subcom].get(index_list[i], 0) + 1

        # Append the community species information to the list
        community_species.append(dict_com)

    # Loop over each community after the first one
    for i in range(len(communities)):
        com = communities[i]
        subcom = community_species[i]

        # Loop over each subcommunity
        for sub in subcom:
            subcom_species = subcom[sub]

            # Loop over each species in the subcommunity
            for spe in subcom_species:
                dict_subcom = {
                    "Community": com,
                    "Subcommunity": sub,
                    "Species": spe,
                    "Number of Appearances": subcom_species[spe],
                }

                # Create a dataframe with the subcommunity species information
                df_to_append = pd.DataFrame([dict_subcom])

                # Append the dataframe to the species community dataframe
                df_species_com = pd.concat(
                    [df_species_com, df_to_append], ignore_index=True
                )

    return df_species_com


def main(
    filepath: str,
    delimiter: str,
    output_comm_statistics: str,
    output_species_comm: str,
) -> None:
    """
    Reads a CSV file, calculates community statistics and species community,
    and saves the results in separate CSV files.

    Args:
        filepath: The path to the CSV file.
        delimiter: The delimiter used in the CSV file.
        output_comm_statistics: The path to save the community statistics CSV file.
        output_species_comm: The path to save the species community CSV file.
    """

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(filepath, sep=delimiter, index_col=0)

    # Calculate community statistics
    df_final = calculate_community_statistics(data)

    # Calculate species community
    df_species_com = calculate_species_community(data)

    # Save community statistics to a CSV file
    df_final.to_csv(output_comm_statistics, sep=delimiter)

    # Save species community to a CSV file
    df_species_com.to_csv(output_species_comm, sep=delimiter, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculates community statistics and species community")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Input CSV file path.",
    )
    parser.add_argument(
        "--delimiter", type=str, default=";", help="Delimiter used in CSV."
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
        args.delimiter,
        args.output+"/output_comm_statistics.csv",
        args.output+"/output_species_comm.csv",
    )
