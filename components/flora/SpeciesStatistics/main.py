import argparse
import pandas as pd

def main(filepath: str, delimiter: str, output_filepath: str):
    """
    Compute statistics for species data from a CSV file and save the results to a new CSV file.

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        output_filepath (str): Path to save the output CSV file with computed statistics.
    """

    # Read data from the input CSV file
    data = pd.read_csv(filepath, sep=delimiter, decimal=".", index_col=0)

    # Define a list of permanent rows to exclude from the analysis
    permanent_rows = [
            "Date",
            "Authors",
            "Group",
            "Project",
            "Community",
            "Community Authors",
            "Community Year",
            "Subcommunity",
            "Subcommunity Authors",
            "Subcommunity Year",
            "Location",
            "MGRS",
            "Latitude",
            "Longitude",
            "Natural Site",
            "Lithology",
            "Coverage(%)",
            "Altitude(m)",
            "Plot slope",
            "Alt. Veg. (cm)",
            "Plot area(m2)",
            "Plot orientation",
            "Ecology",
            "Pictures",
            "Number of Species",
            "Species",
        ]

    # Remove permanent rows from the dataframe
    df = data.drop(axis=0, labels=permanent_rows)
    df = df.replace("+", 0.1)

    # Get species names from the dataframe
    species = df.index.values

    # Initialize lists to store species statistics
    sum_species = []
    coverage_mean_transform = []

    # Compute statistics for each species
    for i in df.index:
        count = 0
        sum_coverage = 0
        coverage_mean = 0
        for c in df.columns:
            if df.loc[i, c] != "-":
                count += 1
                sum_coverage += float(df.loc[i, c])
        coverage_mean = sum_coverage / count

        # Transform coverage mean into categories
        if coverage_mean >= 5:
            coverage_mean_transform.append("75-100")
        elif 5 > coverage_mean >= 4:
            coverage_mean_transform.append("50-75")
        elif 4 > coverage_mean >= 3:
            coverage_mean_transform.append("25-50")
        elif 3 > coverage_mean >= 2:
            coverage_mean_transform.append("5-25")
        elif 2 > coverage_mean >= 1:
            coverage_mean_transform.append("2-5")
        else:
            coverage_mean_transform.append("1-2")

        sum_species.append(count)

    # Calculate the total count of species
    sum_total = sum(sum_species)

    # Calculate species frequency
    species_frecuency = [(elem / sum_total) * 100 for elem in sum_species]

    # Create a new DataFrame to store the results
    output = pd.DataFrame(
        list(zip(species, sum_species, coverage_mean_transform, species_frecuency)),
        columns=["Species", "Sum_Species", "Coverage_mean_percentage", "Species_Frequency"],
    )

    # Save the output DataFrame to a CSV file
    output.to_csv(output_filepath, sep=delimiter, encoding="utf-8-sig", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Species Statistics")

    # Define command-line arguments
    parser.add_argument("--filepath", type=str, required=True, help="Path to the input CSV File")
    parser.add_argument("--delimiter", type=str, required=True, help="Delimiter used in the input CSV File")
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

    # Call the main function with provided arguments and specify the output file path
    main(args.filepath, args.delimiter, args.output+"/species_statistics.csv")
