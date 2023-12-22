import pandas as pd
import plotly.express as px

from argparse import ArgumentParser


def calculate_sum(data_frame: pd.DataFrame):
    """Calculate the sum and accumulative sum of a time series DataFrame.

    This function takes a DataFrame with a "DATE" column and another numerical column
    and calculates the sum and cumulative sum for each hydrological year.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing time series data.

    Returns:
        pd.DataFrame: A DataFrame with columns "years," "total," and "accumulated,"
        representing the hydrological year, the sum for each year, and the cumulative sum
        up to that year, respectively.
    """
    first_year = int(data_frame["DATE"].iloc[0][:4])
    last_year = int(data_frame["DATE"].iloc[-1][:4])

    total = []
    years = []

    for i in range(first_year, last_year):
        year_information = data_frame[
            (data_frame["DATE"] > f"{i}-09-30") & (data_frame["DATE"] < f"{i+1}-10-01")
        ]
        records = year_information[year_information.columns[1:]]
        total.append(records.sum().values[0])
        years.append(i)

    accumulated = pd.Series(total).cumsum()
    final_data_frame = pd.DataFrame(
        {"years": years, "total": total, "accumulated": accumulated}
    )
    return final_data_frame


def station_comparison(
    filepath: str,
    stationA: str,
    stationB: str,
    output: str,
    delimiter: str = ";",
):
    """Compare accumulated precipitation between two stations.

    This function reads a CSV file containing precipitation data for multiple stations,
    compares the accumulated precipitation between two specified stations, and generates
    a scatter plot with a trendline. Then it saves the result as an HTML file.

    Args:
        filepath (str): The path to the CSV file containing precipitation data.
        stationA (str): The name of the first station for comparison.
        stationB (str): The name of the second station for comparison.
        output (str): The path to save the generated scatter plot as an HTML file.
        delimiter (str, optional): The delimiter used in the CSV file (default is ";").

    Returns:
        None
    """
    stationA = stationA.upper()
    stationB = stationB.upper()

    precipitation_data = pd.read_csv(filepath, sep=delimiter, decimal=".")

    if stationA not in precipitation_data.columns:
        raise ValueError(f"Station {stationA} not found in data provided")
    if stationB not in precipitation_data.columns:
        raise ValueError(f"Station {stationB} not found in data provided")

    # Filter data by station
    precipitation_stationA = pd.concat(
        [precipitation_data["DATE"], precipitation_data[stationA]], axis=1
    ).dropna(axis=0, how="any")
    precipitation_stationB = pd.concat(
        [precipitation_data["DATE"], precipitation_data[stationB]], axis=1
    ).dropna(axis=0, how="any")

    precipitation_year_stationA = calculate_sum(precipitation_stationA)
    precipitation_year_stationB = calculate_sum(precipitation_stationB)

    stations_data = pd.merge(
        precipitation_year_stationA,
        precipitation_year_stationB,
        on="years",
        suffixes=(f"_{stationA}", f"_{stationB}"),
    )

    # Plot data

    fig = px.scatter(
        stations_data,
        x=f"accumulated_{stationA}",
        y=f"accumulated_{stationB}",
        hover_data={
            "Year": (":.d", stations_data["years"]),
            f"Precipitations {stationA}": (":.2f", stations_data[f"total_{stationA}"]),
            f"Precipitations {stationB}": (":.2f", stations_data[f"total_{stationB}"]),
            f"accumulated_{stationA}": ":.2f",
            f"accumulated_{stationB}": ":.2f",
        },
        trendline="ols",
        trendline_color_override="#1AABAC",
        title=f"Accumulated precipitation in {stationA} vs {stationB}",
        labels={
            f"accumulated_{stationA}": f"Accumulated {stationA}",
            f"accumulated_{stationB}": f"Accumulated {stationB}",
        },
    )
    fig.update_layout(hovermode="x")
    fig.update_xaxes(
        showspikes=True, spikedash="dot", spikecolor="grey", spikethickness=1
    )
    fig.update_yaxes(
        showspikes=True, spikedash="dot", spikecolor="grey", spikethickness=1
    )
    fig.update_traces(marker=dict(size=10))

    fig.write_html(output, auto_open=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Compare station data")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the precipitation file to be read",
        dest="filepath",
        metavar="STRING",
    )

    parser.add_argument(
        "--stationA",
        type=str,
        required=True,
        help="One of the stations to be compared",
        dest="stationA",
        metavar="STRING",
    )

    parser.add_argument(
        "--stationB",
        type=str,
        required=True,
        help="One of the stations to be compared",
        dest="stationB",
        metavar="STRING",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter used in the file",
        dest="delimiter",
        metavar="CHAR",
    )
    
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Path to the output file",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    station_comparison(
        filepath=args.filepath,
        stationA=args.stationA,
        stationB=args.stationB,
        delimiter=args.delimiter,
        output=args.output+"/output.html",
    )
