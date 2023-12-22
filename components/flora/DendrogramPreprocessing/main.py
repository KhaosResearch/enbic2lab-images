import argparse

import pandas as pd


def clean_data_frame(element):
    """
    Cleans and transforms the given element from a data frame.

    Args:
        element (str): The element to be cleaned.

    Returns:
        float: The cleaned and transformed element.
    """

    # Define a mapping of characters to their corresponding values
    mapping = {"-": 0, "x": 0, "X": 0, ".": 0, "+": 0.2, "+.2": 0.2, "(+)": 0.1}

    # Return the value associated with the given element from the mapping
    return float(mapping.get(element, element))


def main(filepath: str, delimiter: str, output: str) -> None:
    """
    Read a CSV file, transpose it, clean the data, and save it to a new file.

    Args:
        filepath: The path to the CSV file.
        delimiter: The delimiter used in the CSV file.
        output: The path to save the processed data.

    Returns:
        None
    """

    # Read the CSV file
    df = pd.read_csv(filepath, sep=delimiter)

    # Transpose the dataframe
    df_transposed = df.set_index(df.columns[0]).T

    # Remove columns until the first column is 'Species'
    while df_transposed.columns[0] != "Species":
        df_transposed = df_transposed.drop([df_transposed.columns[0]], axis=1)
    else:
        df_transposed = df_transposed.drop(["Species"], axis=1)

    # Generate new column headers
    new_headers = []
    for index, _ in df_transposed.items():
        words = index.split()
        if len(words) == 1:
            new_headers.append(words[0][:4])
        if len(words) > 1:
            new_headers.append(words[0][:4] + " " + words[1][:4])

    # Set the new column headers
    df_transposed = df_transposed.set_axis(new_headers, axis="columns")

    # Clean the data using a custom function
    df_processed = df_transposed.map(clean_data_frame)

    # Save the processed dataframe to a new CSV file
    df_processed.to_csv(output, sep=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transform the flora csv into a DataSet useful for the creation of the dendrogram"
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

    main(
        args.filepath,
        args.delimiter,
        args.output+"/output.csv",
    )
