from datetime import datetime
from enum import Enum
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

import argparse


class Mode(str, Enum):
    continuous = "continuous"
    dividedByYears = "dividedByYears"
    both = "both"


def main(filepath: str, output: str, delimiter: str = ";", mode: str = "both"):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        mode (str): Parameter necessary to calculate the useful rainfall.
        output (str): Path to save the output HTML file.
    """
    # Read input CSV file and convert 'Fecha' column to date type
    df = pd.read_table(filepath, delimiter=delimiter)
    df["Fecha"] = [datetime.strptime(d, "%d/%m/%Y") for d in df["Fecha"]]

    # Create the list that will contain all the figures finally dumped into the HTML output
    figures = list()

    if mode == Mode.dividedByYears or mode == Mode.both:
        # Extract all the years included in the table and eliminate this dimension by means of the column 'Fecha sin año'
        df["Año"] = [d.year for d in df["Fecha"]]
        df["Fecha sin año"] = [d.replace(year=2000) for d in df["Fecha"]]
        years = sorted(list(set(df["Año"])), reverse=True)

        # Create figure
        fig = go.Figure()

        # Plot TMAX and TMIN for each of the years found in the table
        for year in years:

            # Filter the rows corresponding to the current year
            sub_df = df[df["Año"] == year]

            # Add TMAX
            fig.add_trace(
                go.Scatter(
                    x=list(sub_df["Fecha sin año"]),
                    y=list(sub_df["TMAX"]),
                    name=f"Temp max",
                    legendgroup=year,
                    legendgrouptitle=dict(text=year),
                    hovertemplate="%{x} " + str(year) + ", %{y}",
                    visible=True if year == years[0] else "legendonly",
                )
            )

            # Add TMIN
            fig.add_trace(
                go.Scatter(
                    x=list(sub_df["Fecha sin año"]),
                    y=list(sub_df["TMIN"]),
                    name=f"Temp min",
                    legendgroup=year,
                    legendgrouptitle=dict(text=year),
                    hovertemplate="%{x} " + str(year) + ", %{y}",
                    visible=True if year == years[0] else "legendonly",
                )
            )

        # Customize the x-axis labels to eliminate the years
        fig.update_xaxes(dtick="M1", tickformat="%d %b")

        # Set titles
        fig.update_layout(
            title_text="Maximum and minimum temperature per day (grouped by year)",
            yaxis_title="Temperature (°C)",
        )

        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="1 month",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=3,
                                label="3 months",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=6,
                                label="6 months",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(count=1, label="All", step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

        # Add the figure to the list
        figures.append(fig)

    if mode == Mode.continuous or mode == Mode.both:
        # Create figure
        fig = go.Figure()

        # Add TMAX
        fig.add_trace(
            go.Scatter(x=list(df["Fecha"]), y=list(df["TMAX"]), name=f"Temp max")
        )

        # Add TMIN
        fig.add_trace(
            go.Scatter(x=list(df["Fecha"]), y=list(df["TMIN"]), name=f"Temp min")
        )

        # Set titles
        fig.update_layout(
            title_text="Maximum and minimum temperature per day (continuous)",
            yaxis_title="Temperature (°C)",
        )

        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="1 month",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=3,
                                label="3 months",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=6,
                                label="6 months",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=1, label="1 year", step="year", stepmode="todate"
                            ),
                            dict(count=1, label="All", step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

        # Add the figure to the list
        figures.append(fig)

    # Write the figures consecutively in the output HTML file
    for fig in figures:
        with open(output, "a") as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP Plot component")

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
        "--mode",
        type=str,
        required=True,
        default="both",
        help="Type of distribution to be followed in the chart",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output HTML",
        required=True,
        default="/mnt/shared/Temperature_plot.html"
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(args.filepath, args.output, args.delimiter, args.mode)
