import argparse

import pandas as pd


def main(filepath: str, delimiter: str, output: str) -> None:
    """
    Read a CSV file, calculate mean values for specified columns,
    and save the results in a new CSV file.

    Args:
        filepath (str): The path to the input CSV file.
        delimiter (str): The delimiter used in the input CSV file.
        output (str): The path to the output CSV file.

    Returns:
        None
    """

    # Read the CSV file into a DataFrame
    data = pd.read_csv(filepath, sep=delimiter, index_col=0, header=None)

    # Create an empty DataFrame with the desired output columns
    df_final = pd.DataFrame(columns=["Mean Slope", "Mean Orientation"])

    # Calculate the sum of the "Plot orientation" column
    sum_orientation = data.loc["Plot orientation"].dropna().astype(float).sum()

    # Calculate the sum of the "Plot slope" column
    sum_slope = data.loc["Plot slope"].dropna().astype(float).sum()

    # Calculate the sum of the "Alt. Veg. (cm)" column
    sum_alt_veg = data.loc["Alt. Veg. (cm)"].dropna().astype(float).sum()

    # Calculate the total number of columns in the DataFrame
    total_inventory = len(data.columns)

    # Calculate the mean values and assign them to the output DataFrame
    df_final.loc[0, "Mean Orientation"] = round(sum_orientation / total_inventory, 2)
    df_final.loc[0, "Mean Slope"] = round(sum_slope / total_inventory, 2)
    df_final.loc[0, "Mean Alt. Veg. (cm)"] = round(sum_alt_veg / total_inventory, 2)

    # Save the output DataFrame to a CSV file
    df_final.to_csv(output, sep=delimiter, index=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates the mean values for specific columns."
    )
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

    main(args.filepath, args.delimiter, args.output+"/output.csv")
