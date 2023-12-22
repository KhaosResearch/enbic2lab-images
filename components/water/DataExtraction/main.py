import pandas as pd
from numpy import nan
from argparse import ArgumentParser


def data_extraction(
    filepath: str,
    output: str,
    delimiter: str = ";",
) -> None:
    """Extract hydrological data from a CSV file, compute yearly statistics, and save the results.

    Parameters:
    - filepath (str): The path to the input CSV file containing hydrological data.
    - output (str): The path to save the output CSV file with computed statistics.
    - delimiter (str, optional): The delimiter used in the CSV file. Default is ";".

    Returns:
    None

    Usage:
    - This function reads hydrological data from a CSV file, calculates yearly statistics
      for each station, and saves the results in a new CSV file.

    Example:
    ```python
    filepath = "path/to/hydrological_data.csv"
    output_filepath = "path/to/output_statistics.csv"
    data_extraction(filepath, output_filepath, delimiter=";")
    ```
    """
    # create dataframe
    df = pd.read_csv(filepath, sep=delimiter)

    # format to datetime
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")

    # create output dataframe
    output_df = pd.DataFrame(
        columns=[
            "Hidrologic Year",
            "Station",
            "Year Mean",
            "Year Maximum",
            "Year minimum",
            "Year Collected Data",
            "Year Empty Data",
            "Year Collected Data (Percentage)",
            "Year Empty Data (Percentage)",
            "Sum of the Year",
        ]
    )

    min_year = df["DATE"].min().year
    max_year = df["DATE"].max().year
    row = 1
    for station in df.columns.drop("DATE").to_list():
        # Filtering for hidrologic year
        for year in range(min_year, max_year):
            start = f"{year}-10-1"
            end = f"{year + 1}-9-30"
            filtered_df = df.loc[(df["DATE"] >= start) & (df["DATE"] <= end)]

            # Counting the number of rows
            n_rows = len(filtered_df.index)
            # Counting the number of empty rows
            empty_rows = filtered_df[station].isnull().sum()
            # Calculating the percentage of empty rows
            empty_per = (empty_rows / n_rows) * 100

            out_row = [
                f"{year}/{year + 1}",
                station,
                filtered_df[station].mean(),
                filtered_df[station].max(),
                filtered_df[station].min(),
                n_rows - empty_rows,
                empty_rows,
                100 - empty_per,
                empty_per,
                filtered_df[station].sum() if filtered_df[station].sum() != 0 else nan,
            ]

            output_df.loc[row] = out_row

            row += 1

    output_df.to_csv(output, index=False, sep=delimiter)


if __name__ == "__main__":
    parser = ArgumentParser(description="Extract data from a CSV water file")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path of Time Series CSV file",
        required=True,
        metavar="STRING",
        dest="filepath",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of CSV",
        required=False,
        default=";",
        metavar="STRING",
        dest="delimiter",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Output file path",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    data_extraction(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output=args.output+"/StatisticalData.csv",
    )
