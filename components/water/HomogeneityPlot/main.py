import pandas as pd
import plotly.express as px
import re
from datetime import datetime

from argparse import ArgumentParser


def homogeneity_plot(
    filepath_data: str,
    filepath_homogeneity: str,
    data_type: str,
    output: str,
    criteria: str = "r2",
    delimiter: str = ";",
):
    data = pd.read_csv(filepath_data, sep=delimiter, decimal=".")
    homogeneity = pd.read_csv(filepath_homogeneity, sep=delimiter, decimal=".")

    station = data.columns[1]

    cut_date = homogeneity[criteria][1]
    cut_date_miliseconds = datetime.strptime(cut_date, "%Y-%m-%d").timestamp() * 1000

    matches = re.findall(r"mu1=([0-9.]+), mu2=([0-9.]+)", homogeneity[criteria][4])[0]

    match data_type:
        case "temperature":
            plot_title = "Temperature"
            x_label = "Temperature (°C)"
        case "precipitation":
            plot_title = "Precipitation"
            x_label = "Precipitation (mm)"
        case _:
            raise ValueError("Invalid data type")

    bar_size = 1
    fig = px.bar(
        data,
        x="DATE",
        y=data.columns[1],
        title=f"{plot_title} data of {station}<br><sup>Homogeneity test: {criteria}</sup>",
        labels={"DATE": "Date", data.columns[1]: x_label},
        hover_data={
            "Date": (":.d", data["DATE"]),
            x_label: (":.2f", data[data.columns[1]]),
        },
    )
    fig.update_layout(
        hovermode="x",
        legend=dict(title="<b>Legend</b><br>", title_font_size=16, font=dict(size=14)),
        title_font_size=24,
    )
    fig.update_xaxes(
        showspikes=True, spikedash="dot", spikecolor="grey", spikethickness=1
    )
    fig.update_yaxes(
        showspikes=True, spikedash="dot", spikecolor="grey", spikethickness=1
    )
    fig.update_traces(
        width=86400000 * bar_size,
        marker=dict(line=dict(width=0), opacity=0.8, color="#1AABAC"),
    ),
    fig.for_each_trace(lambda t: t.update(name=plot_title))

    fig.add_vline(
        x=cut_date_miliseconds,
        name="Change of homogeneity",
        line_width=3,
        line_dash="dash",
        line_color="#595959",
        annotation_text=f"Change point: {cut_date}",
        annotation_position="top right",
        showlegend=True,
    )

    fig.add_shape(
        type="line",
        x0=datetime.strptime(min(data["DATE"]), "%Y-%m-%d").timestamp() * 1000,
        y0=float(matches[0]),
        x1=cut_date_miliseconds,
        y1=float(matches[0]),
        line_width=3,
        line_dash="dot",
        line_color="orange",
        name=f"Mean before change point<br><sup>mu1={round(float(matches[0]), 3)}</sup>",
        showlegend=True,
    )
    fig.add_shape(
        type="line",
        x0=cut_date_miliseconds,
        y0=float(matches[1]),
        x1=datetime.strptime(max(data["DATE"]), "%Y-%m-%d").timestamp() * 1000,
        y1=float(matches[1]),
        line_width=3,
        line_dash="dot",
        line_color="green",
        name=f"Mean after change point<br><sup>mu2={round(float(matches[1]), 3)}</sup>",
        showlegend=True,
    )

    fig.update_traces(showlegend=True)

    fig.write_html(output, auto_open=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Compare station data")

    parser.add_argument(
        "--filepath-data",
        type=str,
        required=True,
        help="Path to the file to be read",
        dest="filepath_data",
        metavar="STRING",
    )

    parser.add_argument(
        "--filepath-homogeneity",
        type=str,
        required=True,
        help="Path to the file containing the homogeneity information",
        dest="filepath_homogeneity",
        metavar="STRING",
    )

    parser.add_argument(
        "--data-type",
        type=str.lower,
        required=True,
        help="Type of data to be read. Must be 'temperature' or 'precipitation'",
        choices=["temperature", "precipitation"],
        dest="data_type",
        metavar="STRING",
    )

    parser.add_argument(
        "--criteria",
        type=str,
        required=False,
        help="Criteria to be used for the homogeneity test",
        dest="criteria",
        metavar="STRING",
        choices=["Pettit Test", "SNHT Test", "Buishand Test"],
        default="Pettit Test",
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

    homogeneity_plot(
        filepath_data=args.filepath_data,
        filepath_homogeneity=args.filepath_homogeneity,
        data_type=args.data_type,
        criteria=args.criteria,
        delimiter=args.delimiter,
        output=args.output+"/output.html",
    )
