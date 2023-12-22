import pandas as pd
from datetime import datetime
import argparse

def date_range(start, end):
    """[summary]

    Args:
        start ([datetime]): [initial date]
        end ([datetime]): [final date]

    Returns:
        Date Range between start and end date
    """
    date_list = []
    curr_date = start
    while curr_date <= end:
        date_list.append(curr_date)
        curr_date = curr_date.replace(year=curr_date.year + 1)
    return date_list

def main(
    filepath: str,
    output: str,
    initial_year: str = "1991",
    final_year:str="2021",
    date_column:str="fecha",
    delimiter: str = ";"
    
):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str) --> File path of the CSV File.
        initial_year (str) -->  Intial year of the dataset.
        final_year (str) -->  Final year of the dataset
        delimiter (str) --> Delimiter of the CSV File.
        date_column (str) --> Name of the date column.
        output (str) --> Filepath of the output CSV file.
    """
    # Read CSV file
      # Read CSV file
    df = pd.read_csv(filepath, delimiter=delimiter, parse_dates=[date_column], dayfirst=True)
    # Convert 'fecha' column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    # Filter data for the specified years
    df_filtered = df[(df[date_column].dt.year >= int(initial_year)) & (df[date_column].dt.year <= int(final_year))]

    # Calculate mean for each column for each day of the year
    means = df_filtered.groupby(df_filtered[date_column].dt.strftime('%m-%d')).mean()

    # Iterate through rows with missing values and fill with the calculated means
    for index, row in df[df.isnull().any(axis=1)].iterrows():
        date_str = row[date_column].strftime('%m-%d')
        for column in df.columns:
            if pd.isnull(row[column]):
                if date_str in means.index:
                    df.at[index, column] = means.loc[date_str, column]
    # Write the updated DataFrame to a new CSV file
    df.to_csv(output, sep=delimiter, index=False)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataframe mean interpolation for NA values")

    # Define command-line arguments
    parser.add_argument(
        "--filepath", 
        type=str, 
        required=True, 
        help="Path to the input CSV File", 
        default="/mnt/shared/input.csv"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default="Date",
        required=True,
        help="Name of the date column.",
    )
    parser.add_argument(
        "--initial-year",
        type=str,
        default="1991",
        required=False,
        help="Intial year of the dataset.",
    )
    parser.add_argument(
        "--final-year",
        type=str,
        default="2021",
        required=False,
        help=" Final year of the dataset",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help=" Name of the output CSV file.",
    )

    args = parser.parse_args()
    
    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.output,
        args.initial_year,
        args.final_year,
        args.date_column,
        args.delimiter
    )
