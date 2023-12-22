from datetime import datetime
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px


def main(filepath: str, output: str, delimiter: str = ";"):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        output (str): Path to save the output HTML file.
    """

    # Define the path to the output file and delete it if it exists previously
    output_file_path = Path(filepath).parent / output
    if output_file_path.exists():
        output_file_path.unlink()

    # Read input CSV file and convert 'Fecha' column to date type
    df = pd.read_table(filepath, delimiter=delimiter)
    df["Fecha"] = [datetime.strptime(d, "%d/%m/%Y") for d in df["Fecha"]]

    # Extract all the years included in the table
    df["Año"] = [d.year for d in df["Fecha"]]
    years = sorted(list(set(df["Año"])))

    # Declare the list that will contain the annual precipitations
    year_sums = list()

    # Calculate the sum of the precipitation for each year
    for year in years:

        # Filter the rows corresponding to the current year
        sub_df = df[df["Año"] == year]

        # Calculate the sum of the precipitation for the current year
        year_sums.append(np.sum(sub_df["Precipitación"]))

    # Calculate the average annual precipitation
    year_sums_mean = np.mean(year_sums)

    # Calculate the deviation from the average for each year
    devs = year_sums - year_sums_mean

    # Add cumulative annual standard deviation from the mean
    fig = px.area(x=years, y=np.cumsum(devs))

    # Set titles
    fig.update_layout(
        title_text="Cumulative annual standard deviation from the mean",
        yaxis_title="Cumulative annual standard deviation from the mean",
        xaxis_title="Years",
    )

    with open(output_file_path, "a") as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CDFM Precipitation component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the input CSV file with the data needed to build the corresponding graph",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=True,
        default=";",
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output HTML",
        required=True,
        default="/mnt/shared/CDFM_Precipitation_plot.html"
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(args.filepath, args.output, args.delimiter)
