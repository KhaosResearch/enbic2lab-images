from argparse import ArgumentParser
import datetime
import pandas as pd
from numpy import NaN
from tqdm import tqdm
import re


def __get_station_data(data: pd.Series, output_df: pd.DataFrame) -> None:
    """Extracts and stores precipitation data for a station in a time series format.

    This function is used internally to extract and store precipitation data for a specific station in a time series format.

    Args:
        data (pd.Series): A Pandas Series containing the precipitation data for a station.
        output_df (pd.DataFrame): A Pandas DataFrame where the extracted time series data will be stored.

    Returns:
        None

    Example:
        This function is not meant to be directly invoked by users. It is used internally by the 'precipitationMatrixTransformation' function to extract and store precipitation data for each station in a time series format.

    Note:
        - The function iterates through the 'P1' to 'P31' columns of the input data Series, extracts the values and their corresponding dates, and stores them in the output DataFrame.
        - It handles missing or invalid dates by skipping them and does not raise errors for such cases.
    """

    values_p = data["P1":"P31"].to_dict()
    for key, val in values_p.items():
        try:
            datetime_index = datetime.datetime(
                int(data["AÑO"]), int(data["MES"]), int(key.replace("P", ""))
            )
            output_df.loc[datetime_index] = val
        except ValueError:
            None


def precipitation_matrix_transformation(
    filepath: str,
    output: str,
    delimiter: str = ";",
) -> None:
    """Transforms a precipitation data matrix into a time series format.

    This function takes a precipitation data matrix in a CSV file and transforms it into a time series format. It replaces missing or invalid precipitation values with 0 and rescales the values. The resulting time series covers a date range based on the data.

    Args:
        filepath (str): The path to the CSV file containing the precipitation data matrix.
        output (str): The path to the output CSV file for the transformed time series data.
        delimiter (str): The delimiter used in the CSV file (default: ";").

    Returns:
        None

    Example:
        To transform a precipitation data matrix and save the time series data to an output file:

        >>> precipitationMatrixTransformation("input_data.csv", "output_time_series.csv")

    Note:
        - IMPORTANT: This function may take a long time to run depending on the size of the input data.
        - It replaces missing or invalid precipitation values with 0.
        - The resulting time series data is saved to the specified output file in a CSV format.
    """

    # create dataframe
    matrix_df = pd.read_csv(filepath, sep=delimiter, encoding="utf8")

    # replace precipitation with values -3 and -4 to 0
    matrix_df = matrix_df.replace([-3, -4], 0)
    matrix_df.loc[:, "P1":"P31"] = matrix_df.loc[:, "P1":"P31"].div(10)

    # Calculate the start and end dates based on the data
    min_date = matrix_df[["AÑO", "MES"]].min()
    max_date = matrix_df[["AÑO", "MES"]].max()
    start_date = (
        f"{min_date['AÑO']-1}-10-01"
        if min_date["MES"] <= 10
        else f"{min_date['AÑO']}-10-01"
    )
    end_date = (
        f"{max_date['AÑO']+1}-09-30"
        if max_date["MES"] >= 10
        else f"{max_date['AÑO']}-09-30"
    )

    # Create a date range for the time series
    dates_pd = pd.date_range(start=start_date, end=end_date, freq="D")

    # create dataframe where the time series data is to be stored
    final_pd = pd.DataFrame(index=dates_pd)

    # get the stations where the data is obtained
    grouped_data = matrix_df.groupby("NOMBRE")

    # create a dataframe to each station that will be used to get the final output
    # TODO -> This for loop creates a bottleneck with complexity of O(n*m*p) which in the worst case is O(n^3). It should be improved, maybe using multiprocessing
    for station, data_station in tqdm(grouped_data):
        partial_df = pd.DataFrame(columns=[station])

        data_station.apply(lambda row: __get_station_data(row, partial_df), axis=1)

        final_pd = pd.concat([final_pd, partial_df], axis=1)

    # drop columns with NaN values
    if NaN in final_pd.columns:
        final_pd = final_pd.drop(NaN, axis="columns")

    final_pd.reset_index(inplace=True)
    final_pd.rename(columns={"index": "DATE"}, inplace=True)

    final_pd.to_csv(output, sep=delimiter, index=False)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path of a precipitation CSV file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of CSV",
        required=False,
        default=";",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path of the output CSV file",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    precipitation_matrix_transformation(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output=args.output + "/PrecipitationTimeSeries.csv",
    )
