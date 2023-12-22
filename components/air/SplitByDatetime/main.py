import pandas as pd
import argparse

def split_by_datetime(filepath: str,
                      delimiter: str,
                      date_column: str,
                      start_date: str,
                      end_date: str,
                      output: str):
    """
    Given a pandas dataset and start date/end date, select a portion of this dataset
    
    Date format: 'yyyy-mm-dd'
    
    Returns a portion of the original dataset
    """
    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter)

    # Convert date_column to datetime type if it's not already in datetime format
    dataframe[date_column] = pd.to_datetime(dataframe[date_column])

    # Parse start_date and end_date as datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter dataframe based on the specified date range
    mask = (dataframe[date_column] >= start_date) & (dataframe[date_column] <= end_date)
    filtered_dataframe = dataframe.loc[mask]

    # Save Outfile
    filtered_dataframe.to_csv(output, sep=delimiter, index=None)


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the altitude range of each community.")
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/scaled_dataset.csv",
        help="Input CSV file path.",
    )
    parser.add_argument("--delimiter", type=str, default=";", help="Delimiter used in CSV.")
    parser.add_argument("--date-column", type=str, default="fecha", help="Date column name")
    parser.add_argument("--start-date", type=str, default="1992-01-01", help="Select start date to split the dataset")
    parser.add_argument("--end-date", type=str, default="2021-01-01", help="Select end date to split the dataset")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/split_dataset.csv",
        help="Output CSV file path.",
    )
    args = parser.parse_args()
    split_by_datetime(args.filepath, args.delimiter, args.date_column, args.start_date, args.end_date,
                      args.output)
