import datetime
import pandas as pd
from tqdm import tqdm
from numpy import NaN

from enum import Enum
from argparse import ArgumentParser


class max_or_min(Enum):
    MAX = "TMAX"
    MIN = "TMIN"


def __get_station_data(data: pd.Series, output_df: pd.DataFrame, type: max_or_min) -> None:
    """Extracts and stores temperature data for a station in a time series format.

    This function is used internally to extract and store temperature data for a specific station in a time series format.

    Args:
        data (pd.Series): A Pandas Series containing the tempereature data for a station.
        output_df (pd.DataFrame): A Pandas DataFrame where the extracted time series data will be stored.
        type (max_or_min): A string indicating if the data is for maximum or minimum temperature.

    Returns:
        None

    Example:
        This function is not meant to be directly invoked by users. It is used internally by the 'temperatureMatrixTransformation' function to extract and store precipitation data for each station in a time series format.

    Note:
        - It handles missing or invalid dates by skipping them and does not raise errors for such cases.
    """

    if type == max_or_min.MAX:
        values_p = data["TMAX1":"TMAX31"].to_dict()
        for key, val in values_p.items():
            try:
                datetime_index = datetime.datetime(
                    int(data["AÑO"]), int(data["MES"]), int(key.replace("TMAX", ""))
                )
                output_df.loc[datetime_index] = val
            except ValueError:
                None
    else:
        values_p = data["TMIN1":"TMIN31"].to_dict()
        for key, val in values_p.items():
            try:
                datetime_index = datetime.datetime(
                    int(data["AÑO"]), int(data["MES"]), int(key.replace("TMIN", ""))
                )
                output_df.loc[datetime_index] = val
            except ValueError:
                None
    

def temperatureMatrixTransformation(
    filepath: str,
    output_min: str,
    output_max: str,
    delimiter: str = ";",
):
    """Transforms a temperature data matrix into a time series format.

    This function takes a temperature data matrix in a CSV file and transforms it into a time series format. It replaces missing or invalid temperature values with 0 and rescales the values. The resulting time series covers a date range based on the data.

    Args:
        filepath (str): The path to the CSV file containing the temperature data matrix.
        output_min (str): The path to the output CSV file for the transformed time series data for minimum temperature.
        output_max (str): The path to the output CSV file for the transformed time series data for maximum temperature.
        delimiter (str): The delimiter used in the CSV file (default: ";").
    
    Returns:
        None
    
    Example:
        To transform a temperature data matrix and save the time series data to an output file:

        >>> temperatureMatrixTransformation("input_data.csv", "output_time_series.csv")
    
    Note:
        - The function iterates through the 'TMAX1' to 'TMAX31' columns of the input data Series, extracts the values and their corresponding dates, and stores them in the output DataFrame.
        - It handles missing or invalid dates by skipping them and does not raise errors for such cases.
    """
    # create dataframe
    matrix_df = pd.read_excel(filepath)

    # change column name if it is wrong
    if "AﾑO" in matrix_df.columns:
        matrix_df.rename(columns={"AﾑO": "AÑO"}, inplace=True)

    # divide by 10 to obtain temperatures in the right scale
    matrix_df.loc[:, "TMAX1":"TMIN31"] = matrix_df.loc[:, "TMAX1":"TMIN31"].div(10)
    
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
    final_max_pd = pd.DataFrame(index=dates_pd)

    final_min_pd = pd.DataFrame(index=dates_pd)

    # get the stations where the data is obtained
    grouped_data = matrix_df.groupby("NOMBRE")

    for station, data_station in tqdm(grouped_data):
        partial_tmax_df = pd.DataFrame(columns=[station])
        partial_tmin_df = pd.DataFrame(columns=[station])

        data_station.apply(lambda row: __get_station_data(row, partial_tmax_df, max_or_min.MAX), axis=1)
        data_station.apply(lambda row: __get_station_data(row, partial_tmin_df, max_or_min.MIN), axis=1)

        final_max_pd = pd.concat([final_max_pd, partial_tmax_df], axis=1)
        final_min_pd = pd.concat([final_min_pd, partial_tmin_df], axis=1)
    
    # drop columns with NaN values
    if NaN in final_max_pd.columns:
        final_max_pd = final_max_pd.drop(NaN, axis="columns")
    
    if NaN in final_min_pd.columns:
        final_min_pd = final_min_pd.drop(NaN, axis="columns")
    
    final_max_pd.reset_index(inplace=True)
    final_max_pd.rename(columns={"index": "DATE"}, inplace=True)    

    final_min_pd.reset_index(inplace=True)
    final_min_pd.rename(columns={"index": "DATE"}, inplace=True)    

    # save to csv
    final_max_pd.to_csv(output_max, sep=delimiter, index=False)
    final_min_pd.to_csv(output_min, sep=delimiter, index=False)
        

if __name__ == "__main__":
    parser = ArgumentParser(description="Temperature Matrix Transformation")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the input Excel File",
        dest="filepath",
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter used in the output CSV File",
        dest="delimiter",
        metavar="CHAR"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Path to the output CSV File",
        dest="output",
        metavar="STRING"
    )

    args = parser.parse_args()

    temperatureMatrixTransformation(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output_min=args.output+"/MinTempTimeSeries.csv",
        output_max=args.output+"/MaxTempTimeSeries.csv",
    )