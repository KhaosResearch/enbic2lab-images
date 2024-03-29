import argparse
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from numpy import savetxt
from typing import Tuple


def minmax_scaler(df: pd.DataFrame) -> Tuple[pd.DataFrame, MinMaxScaler]:
    """
    Given a pandas dataframe, it is normalized with MinMaxScaler

    Returns a normalized dataframe and its scaler
    """
    scaler = MinMaxScaler()
    scaler.fit(df)
    scaled_data = scaler.transform(df)
    return scaled_data, scaler


def data_normalization(
    filepath: str,
    delimiter: str,
    pollen_column: str,
    date_column: str,
    output_path: str,
):
    """
    Given a pandas dataframe, it's split in two dataframes (features and target) and then they are normalized with MinMaxScaler

    Returns two normalized dataframes (features and target) and their scalers
    """

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col=date_column)

    # Split features and target to normalize
    target_df = dataframe[[pollen_column]]
    data = dataframe.drop([pollen_column], axis=1)

    scaled_data, _ = minmax_scaler(data)
    scaled_target, _ = minmax_scaler(target_df)

    # Save numpy array as CSV
    suffix = ".csv"
    path_scaled_data = Path(output_path, "scaled_features").with_suffix(suffix)
    path_scaled_target = Path(output_path, "scaled_target").with_suffix(suffix)
    path_data = Path(output_path, "features").with_suffix(suffix)
    path_target = Path(output_path, "target").with_suffix(suffix)

    savetxt(path_data, data, delimiter=delimiter)
    savetxt(path_target, target_df, delimiter=delimiter)
    savetxt(path_scaled_data, scaled_data, delimiter=delimiter)
    savetxt(path_scaled_target, scaled_target, delimiter=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Data Normalization for time series data"
    )
    parser.add_argument(
        "--filepath",
        type=str,
        default="community_altitude_range.csv",
        help="Input CSV file path.",
    )
    parser.add_argument(
        "--delimiter", type=str, default=";", help="Delimiter used in CSV."
    )
    parser.add_argument("--pollen-column", type=str, help="Name of pollen column")
    parser.add_argument(
        "--date-column", type=str, default="fecha", help="Name of the date column"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        help="Output path.",
    )
    args = parser.parse_args()

    data_normalization(
        args.filepath, args.delimiter, args.pollen_column, args.date_column, args.output
    )