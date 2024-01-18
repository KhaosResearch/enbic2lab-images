from datetime import datetime
from operator import itemgetter
from re import sub, findall
from argparse import ArgumentParser
from typing import List

import pandas as pd
import pyhomogeneity
from sklearn.linear_model import LinearRegression


def __prepare_date_dataframe(df, df_filter, start_date, end_date):
    """Prepare the date-based DataFrame for the specified date range.

    This function prepares a DataFrame based on the specified date range by filtering
    and validating the date values.

    Args:
        df (pd.DataFrame): The original DataFrame containing the time series data.
        df_filter (pd.DataFrame): The DataFrame to be filtered and prepared.
        start_date (str): The start date for the date range (in the format "%Y-%m-%d").
        end_date (str): The end date for the date range (in the format "%Y-%m-%d").

    Returns:
        df_filter (pd.DataFrame): The filtered and prepared DataFrame based on the specified date range.

    Raises:
        ValueError: If the provided date range is invalid or outside the available data range.
    """
    df["index"] = df.index
    first_element = df_filter.iloc[0,]["index"]
    last_element = df_filter.iloc[-1,]["index"]
    date = df.iloc[int(first_element) : int(last_element) + 1,]["DATE"]
    df_filter["DATE"] = date
    df_filter = df_filter.drop(["index"], axis=1)

    start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    if (
        start_date_datetime > end_date_datetime
        or datetime.strptime(df_filter.iloc[0,]["DATE"], "%Y-%m-%d")
        > start_date_datetime
    ) or (
        datetime.strptime(df_filter.iloc[-1,]["DATE"], "%Y-%m-%d") < end_date_datetime
    ):
        raise ValueError(
            f"Enter a valid range of dates. Values are stored between {df_filter.iloc[0,]['DATE']} and {df_filter.iloc[-1,]['DATE']}."
        )

    df_filter = df_filter[
        (df_filter["DATE"] >= start_date) & (df_filter["DATE"] <= end_date)
    ]

    return df_filter


def __check_station_names(df, target_station, analysis_stations):
    """Check the validity of station names in the DataFrame.

    This function checks if the target station and analysis station names are valid
    columns in the DataFrame and if each station contains at least one value.

    Args:
        df (pd.DataFrame): The DataFrame containing the time series data.
        target_station (str): The name of the target station for analysis.
        analysis_stations (List[str]): A list of station names for analysis.

    Raises:
        ValueError: If the target station or any of the analysis stations are not valid
            column names or if any station does not contain at least one value.
    """
    columns = list(df.columns)
    columns.remove("DATE")
    columns.remove("index")
    if target_station not in columns:
        raise ValueError(
            f"{target_station} is not a valid column name, valid names: {columns}"
        )
    if len(df[target_station].dropna()) == 0:
        raise ValueError("All the stations must contain at least a value")
    for station in analysis_stations:
        if station not in columns:
            raise ValueError(
                f"{station} is not a valid column name, valid names: {columns}"
            )
        if len(df[station].dropna()) == 0:
            raise ValueError("All the stations must contain at least a value")


def __perform_linear_regression(
    df, target_station, analysis_stations, series_completion
):
    """
    Perform linear regression analysis on data.

    This function conducts linear regression analysis for the target station with
    the specified analysis stations and updates the series completion data.

    Args:
        df (pd.DataFrame): The DataFrame containing the time series data.
        target_station (str): The name of the target station for analysis.
        analysis_stations (List[str]): A list of station names for analysis.
        series_completion (pd.DataFrame): The DataFrame containing DATE and series data.

    Returns:
        analysis_df (pd.DataFrame): A DataFrame containing the results of linear regression analysis,
            including R2, slope, pair of data, and intercept for each analysis station.
        series_completion (pd.DataFrame): The updated series completion data with predicted values.
    """
    analysis_df = pd.DataFrame(
        index=["R2", "Slope", "Pair of data", "Intercept"], columns=analysis_stations
    )
    series_completion = series_completion.set_index("DATE")

    for station in analysis_stations:
        join_df = df[[target_station, station]]
        shared_data = len(join_df.dropna())
        if shared_data == 0:
            y = join_df[station].values.reshape(-1, 1)
        else:
            join_df = join_df.dropna()
            y = join_df[target_station].values.reshape(-1, 1)

        X = join_df[station].values.reshape(-1, 1)
        regr = LinearRegression()
        regr.fit(X, y)

        analysis_df.loc["R2", station] = regr.score(X, y)
        analysis_df.loc["Slope", station] = regr.coef_[0][0]
        analysis_df.loc["Pair of data", station] = shared_data
        analysis_df.loc["Intercept", station] = regr.intercept_[0]

        completion = df[["DATE", station]].dropna()
        completion = completion.set_index("DATE")
        station_fit = completion[station].values.reshape(-1, 1)
        station_pred = regr.predict(station_fit)
        completion[station] = station_pred
        series_completion = series_completion.join(completion)

    return analysis_df, series_completion


def __get_best_stations(completion_criteria, analysis_df, analysis_stations):
    """Get the best stations based on specified completion criteria.

    This function determines the best stations for data completion based on the specified
    completion criteria and the analysis results.

    Args:
        completion_criteria (List[str]): A list of completion criteria, including "r2",
            "slope", and "pair".
        analysis_df (pd.DataFrame): The DataFrame containing analysis results for the stations.
        analysis_stations (List[str]): A list of station names for analysis.

    Returns:
        best_stations (List[str]): A list of the best stations for data completion based on the criteria.
    """
    stations_dict = {station: 0 for station in analysis_stations}
    max_values = analysis_df.max(axis=1)
    analysis_list = list(analysis_df.columns)

    for criteria in completion_criteria:
        for station in analysis_list:
            criteria = criteria.lower()
            if criteria == "r2" and analysis_df[station]["R2"] == max_values["R2"]:
                stations_dict[station] += 1
            if (
                criteria == "pair"
                and analysis_df[station]["Pair of data"] == max_values["Pair of data"]
            ):
                stations_dict[station] += 1
            if (
                criteria == "slope"
                and analysis_df[station]["Slope"] == max_values["Slope"]
            ):
                stations_dict[station] += 1

    stations_sorted = dict(
        sorted(stations_dict.items(), key=itemgetter(1), reverse=True)
    )
    stations_df = pd.DataFrame.from_dict(
        stations_sorted, orient="index", columns=["ocurrences"]
    )
    analysis_ocurrences = stations_df.join(analysis_df.T)

    match completion_criteria[0]:
        case "r2":
            criteria = "R2"
        case "pair":
            criteria = "Pair of data"
        case "slope":
            criteria = "Slope"

    analysis_ocurrences = analysis_ocurrences.sort_values(
        ["ocurrences", criteria], ascending=False
    )
    analysis_df = analysis_ocurrences.drop(["ocurrences"], axis=1).T

    best_stations = list(analysis_df.columns)
    return best_stations


def __complete_target_station(
    best_stations, target_station, series_completion, filtered_df, analysis_df
):
    """Complete the data for the target station based on best stations.

    This function completes the data for the target station using the best stations'
    data and removes intercept values from the completed data.

    Args:
        best_stations (List[str]): A list of best stations for data completion.
        target_station (str): The name of the target station to complete.
        series_completion (pd.DataFrame): The DataFrame containing DATE and series data.
        filtered_df (pd.DataFrame): The DataFrame containing the filtered data.
        analysis_df (pd.DataFrame): The DataFrame containing analysis results.

    Returns:
        completed_data (pd.DataFrame): The completed data for the target station, excluding intercept values.
        target_completion (pd.DataFrame): The target station data with NaNs replaced by best stations' values.
    """
    target_completion = filtered_df[["DATE", target_station]]
    target_completion = target_completion.set_index("DATE")

    completed_data = target_completion[target_completion[target_station].isna()]

    rows_to_complete = target_completion[target_station].isna().sum().tolist()

    if rows_to_complete != 0:
        for station in best_stations:
            target_completion.loc[
                target_completion[target_station].isna(), target_station
            ] = series_completion.loc[
                target_completion[target_station].isna(), station
            ].values
            completed_data = completed_data.fillna(target_completion)

    intercepts = analysis_df.loc["Intercept"].values
    for num in intercepts:
        completed_data = completed_data.replace(num, 0)
        target_completion = target_completion.replace(num, 0)

    return completed_data, target_completion


def __compute_homogeneity_tests(tests, target_completion):
    """Compute homogeneity tests on completed data.

    This function performs homogeneity tests on the completed data of the target station
    using the specified tests. This function is used inside the series_completion function.

    Args:
        tests (List[str]): A list of homogeneity tests to perform, including "pettit",
            "snht", and "buishand".
        target_completion (pd.DataFrame): The completed data of the target station.

    Returns:
        tests_df (pd.DataFrame): A DataFrame containing the results of homogeneity tests, including
            homogeneity, change point location, p-value, maximum test statistics, and average
            between change points for each test.
    """
    tests_df = pd.DataFrame(
        index=[
            "Homogeneity",
            "Change Point Location",
            "P-value",
            "Maximum test Statistics",
            "Average between change point",
        ]
    )
    for test in tests:
        test_name = ""
        match test.lower():
            case "pettit":
                (
                    homogeneity,
                    change_point,
                    p_value,
                    max_stats,
                    avg,
                ) = pyhomogeneity.pettitt_test(target_completion, alpha=0.5, sim=10000)
                test_name = "Pettit Test"
            case "snht":
                (
                    homogeneity,
                    change_point,
                    p_value,
                    max_stats,
                    avg,
                ) = pyhomogeneity.snht_test(target_completion, alpha=0.5, sim=10000)
                test_name = "SNHT Test"
            case "buishand":
                (
                    homogeneity,
                    change_point,
                    p_value,
                    max_stats,
                    avg,
                ) = pyhomogeneity.buishand_range_test(
                    target_completion, alpha=0.5, sim=10000
                )
                test_name = "Buishand Test"
            case _:  # default, if  test not valid -> next test
                continue

        tests_df[test_name] = [
            homogeneity,
            datetime.strptime(target_completion.index[change_point], "%Y-%m-%d").date(),
            p_value,
            max_stats,
            avg,
        ]

    return tests_df


def series_completion(
    filepath: str,
    start_date: str,
    end_date: str,
    target_station: str,
    analysis_stations: List[str],
    output_completed_data: str,
    output_analysis: str,
    output_target_completion: str,
    output_tests: str,
    completion_criteria: List[str] = ["r2", "slope", "pair"],
    tests: List[str] = ["pettit", "snht", "buishand"],
    delimiter: str = ";",
):
    """Completes time series data and performs analysis.

    This function reads a CSV file containing time series data, performs data
    completion for a target station, and conducts various analyses. It also
    performs homogeneity tests on the completed data.

    Args:
        filepath (str): The path to the CSV file containing the time series data.
        start_date (str): The start date for the data analysis.
        end_date (str): The end date for the data analysis.
        target_station (str): The name of the target station to complete.
        analysis_stations (List[str]): A list of station names for analysis.
        output_completed_data (str): The path to save the completed data.
        output_analysis (str): The path to save the analysis results.
        output_target_completion (str): The path to save the target station completion.
        output_tests (str): The path to save the results of homogeneity tests.
        completion_criteria (List[str], optional): A list of completion criteria,
            including "r2", "slope", and "pair" (default is ["r2", "slope", "pair"]).
        tests (List[str], optional): A list of homogeneity tests to perform,
            including "pettit", "snht", and "buishand" (default is ["pettit", "snht", "buishand"]).
        delimiter (str, optional): The delimiter used in the CSV file (default is ";").

    Returns:
        None
    """
    df = pd.read_csv(filepath, sep=delimiter)

    if any(crit not in ["r2", "slope", "pair"] for crit in completion_criteria):
        raise ValueError(
            "Invalid completion criteria. Possible values are 'r2','slope','pair'."
        )
    
    if any(test not in ["pettit", "snht", "buishand"] for test in tests):
        raise ValueError(
            "Invalid homogeneity tests. Possible values are 'pettit','snht','buishand'."
        )     

    df_filter = df.iloc[:, 1:]
    df_filter = df_filter.dropna(how="all")
    df_filter["index"] = df_filter.index
    df_filter = __prepare_date_dataframe(df, df_filter, start_date, end_date)

    __check_station_names(df, target_station, analysis_stations)

    series_completion = pd.DataFrame(columns=["DATE"])
    series_completion["DATE"] = df_filter["DATE"]

    analysis_df, series_completion = __perform_linear_regression(
        df, target_station, analysis_stations, series_completion
    )

    best_stations = __get_best_stations(
        completion_criteria, analysis_df, analysis_stations
    )

    completed_data, target_completion = __complete_target_station(
        best_stations, target_station, series_completion, df_filter, analysis_df
    )

    tests_df = __compute_homogeneity_tests(tests, target_completion)

    target_station = sub("[()]", "", target_station)

    completed_data.to_csv(output_completed_data, sep=delimiter)
    analysis_df.to_csv(output_analysis, sep=delimiter)
    target_completion.to_csv(output_target_completion, sep=delimiter)
    tests_df.to_csv(output_tests, sep=delimiter)


if __name__ == "__main__":
    parser = ArgumentParser(description="Series Completion")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV with the time series data",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date of the time series",
        required=True,
        default="1993-10-01",
        dest="start_date",
        metavar="STRING",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="End date of the time series",
        required=True,
        default="2018-12-31",
        dest="end_date",
        metavar="STRING",
    )
    parser.add_argument(
        "--target-station",
        type=str,
        help="Target station to complete",
        required=True,
        dest="target_station",
        metavar="STRING",
    )
    parser.add_argument(
        "--analysis-stations",
        type=str,
        help="List of stations that will be used to complete the target station.",
        required=True,
        dest="analysis_stations",
        metavar="STRING",
    )
    parser.add_argument(
        "--completion-criteria",
        type=str,
        help="List of criteria that will be used to complete the target station. Values that can be included in the list are 'r2','slope','pair'. By default, every criteria will be used.",
        required=False,
        default="r2, slope, pair",
        dest="completion_criteria",
        metavar="STRING",
    )
    parser.add_argument(
        "--tests",
        type=str,
        help="Homogeneity tests to perform. Values that can be included in the list are 'pettit','snht','buishand'. By default, every test will be performed.",
        required=False,
        default="pettit, snht, buishand",
        dest="tests",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of CSV. By default, the delimiter is ';'",
        required=False,
        default=";",
        dest="delimiter",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to save the output files",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    args.analysis_stations = findall(r'\s*([^,]+)\s*', args.analysis_stations)
    args.completion_criteria = args.completion_criteria.replace(" ", "").split(",")
    args.tests = args.tests.replace(" ", "").split(",")

    series_completion(
        filepath=args.filepath,
        start_date=args.start_date,
        end_date=args.end_date,
        target_station=args.target_station,
        analysis_stations=args.analysis_stations,
        completion_criteria=args.completion_criteria,
        tests=args.tests,
        delimiter=args.delimiter,
        output_completed_data=args.output+"/CompletedData.csv",
        output_analysis=args.output+"/StationsAnalysis.csv",
        output_target_completion=args.output+"/TargetCompleted.csv",
        output_tests=args.output+"/HomogeneityTests.csv",
    )
