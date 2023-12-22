import argparse
from datetime import datetime
from pathlib import Path
import numpy as np

import pandas as pd
import plotly.graph_objects as go


def main(filepath: str, output: str, delimiter: str = ";"):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        output (str): Path to save the output CSV file with computed LLU.
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

    # Declare the lists that will contain the annual sum of each of the measures
    year_esc_sums = list()
    year_inf_sums = list()
    year_llu_sums = list()
    year_prec_sums = list()

    # Calculate the sum of each measure for each year
    for year in years:

        # Filter the rows corresponding to the current year
        sub_df = df[df["Año"] == year]

        # Calculate the sum of each measure for the current year
        year_esc_sums.append(np.sum(sub_df["ESC"]))
        year_inf_sums.append(np.sum(sub_df["INF"]))
        year_llu_sums.append(np.sum(sub_df["LLU"]))
        year_prec_sums.append(np.sum(sub_df["Precipitación"]))

    # Create figure
    fig = go.Figure()

    # Add ESC
    fig.add_trace(go.Bar(x=years, y=year_esc_sums, name="ESC"))

    # Add INF
    fig.add_trace(go.Bar(x=years, y=year_inf_sums, name="INF"))

    # Add LLU
    fig.add_trace(go.Scatter(x=years, y=year_llu_sums, name="LLU"))

    # Add Precipitation
    fig.add_trace(go.Scatter(x=years, y=year_prec_sums, name="Precipitation"))

    # Set titles
    fig.update_layout(
        title_text="Runoff and infiltration",
        yaxis_title="Precipitation (mm)",
        xaxis_title="Years",
    )

    with open(output_file_path, "a") as f:
        f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Precipitation series plot component")

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
        default="/mnt/shared/Precipitation_series_plot.html"
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(args.filepath, args.output, args.delimiter)
