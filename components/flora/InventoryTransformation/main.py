import pandas as pd
import numpy as np
import argparse

def main(filepath: str, delimiter: str, output: str) -> None:
    """
    Transpose a CSV file, transform its values, and restructure the data.

    Args:
        filepath (str): Input CSV file path.
        delimiter (str): Delimiter used in the CSV.
        output (str): Output CSV file path.

    Returns:
        None
    """

    # Read the CSV file and transpose the data
    data = pd.read_csv(filepath, sep=delimiter)
    data = data.transpose()
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header
    # Transform Dataframe values
    for index in data.index:
        data = data.replace("-1", np.nan)
        data.loc[index, "Plot slope"] = round(
            (float(data.loc[index, "Plot slope"]) * 1.6 * 100) / 288, 2
        )

        # Map Plot orientation values to degrees
        orientation_mapping = {
            "N": "0",
            "NNE": "22.5",
            "NE": "45",
            "ENE": "67.5",
            "E": "90",
            "ESE": "112.5",
            "SE": "135",
            "SSE": "157.5",
            "S": "180",
            "SSW": "202.5",
            "SW": "225",
            "WSW": "247.5",
            "W": "270",
            "WNW": "292.5",
            "NW": "315",
            "NNW": "337.5"
        }
        data.loc[index, "Plot orientation"] = orientation_mapping.get(
            data.loc[index, "Plot orientation"], data.loc[index, "Plot orientation"]
        )

    # Permanent columns that should not be modified
    permanent_columns = [
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
    ]

    # Create an auxiliary DataFrame with non-permanent columns
    df2 = data.drop(permanent_columns, axis=1)
    df2_columns = df2.columns
    df2 = df2.fillna("-")
    df2 = df2.replace(["\..*"], "", regex=True)

    # Remove non-permanent columns from the original DataFrame and join with df2
    data = data.drop(df2_columns, axis=1)
    data = data.join(df2)

    # Insert a "No. of register (ID)" column and reset the index
    data.insert(0, "0", data.index)
    data = data.reset_index(drop=True)
    data = data.rename(columns={"0": "No. of register (ID)"})
    data = data.T
    # Save the resulting DataFrame to the output CSV file
    data.to_csv(output, sep=delimiter, header=None)
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
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )
    args = parser.parse_args()

    # Call the main function with command-line arguments
    main(args.filepath, args.delimiter, args.output+"/inventory_transformation.csv")