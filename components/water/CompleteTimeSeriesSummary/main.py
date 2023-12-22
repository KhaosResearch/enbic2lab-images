import pandas as pd
from argparse import ArgumentParser


def complete_timeseries_summary(
    filepath_completed: str,
    filepath_replaced: str,
    output: str,
    color: str = "cyan",
    delimiter: str = ";",
) -> None:
    """Generate a styled HTML summary from completed and replaced time series data.

    Parameters:
    - filepath_completed (str): The path to the CSV file containing completed time series data.
    - filepath_replaced (str): The path to the CSV file containing replaced time series data.
    - output (str): The desired path and filename for the output HTML file.
    - color (str, optional): The background color for replaced data. Default is "cyan".
    - delimiter (str, optional): The delimiter used in the CSV files. Default is ";".

    Returns:
    None

    Usage:
    - This function reads completed and replaced time series data from CSV files,
      highlights the replaced data in the completed time series, and generates a styled HTML summary.

    Example:
    ```python
    filepath_completed = "path/to/completed_data.csv"
    filepath_replaced = "path/to/replaced_data.csv"
    output_html = "path/to/output_summary.html"
    CompleteTimeSeriesSummary(filepath_completed, filepath_replaced, output_html, color="yellow")
    ```
    """
    df_completed = pd.read_csv(filepath_completed, sep=delimiter)
    df_replace = pd.read_csv(filepath_replaced, sep=delimiter)

    station_name = df_completed.columns.tolist()[1]

    def hightlight_completed_data(row):
        background = ["" for _ in row.index]
        if row.DATE in df_replace["DATE"].tolist():
            background[row.index.get_loc(station_name)] = f"background-color: {color}"
        return background

    df_styled = df_completed.style.apply(hightlight_completed_data, axis=1)

    df_styled.format({station_name: "{:.3f}"})
    styles = [
        {
            "selector": "",
            "props": [
                ("border-collapse", "collapse"),
                ("border-color", "rgba(0, 0, 0, 0)"),
                ("border-style", "solid"),
                ("border-width", "2px"),
                ("font-family", '"Helvetica Neue", Helvetica, Arial, sans-serif'),
                ("font-size", "16px"),
                ("line-height", "20px"),
                ("text-size-adjust", "100%"),
                ("cursor", "default"),
                ("width", "max-content"),
                ("margin-left", "auto"),
                ("margin-right", "auto"),
                ("-webkit-border-horizontal-spacing", "0px"),
                ("-webkit-border-vertical-spacing", "0px"),
                ("-webkit-tap-highlight-color", "rgba(0, 0, 0, 0)"),
            ],
        },
        {
            "selector": "tr",
            "props": [
                ("background-color", "white"),
            ],
        },
        {
            "selector": "thead tr",
            "props": [
                ("border-bottom-color", "rgba(0, 0, 0, 100)"),
                ("border-bottom-style", "solid"),
                ("background-color", "rgb(230, 230, 230)"),
            ],
        },
        {"selector": "tbody tr:hover", "props": [("filter", "brightness(0.85);")]},
        {
            "selector": "tbody td",
            "props": [
                ("text-align", "center"),
                ("padding-top", "5px"),
                ("padding-bottom", "5px"),
                ("padding-inline", "3em"),
            ],
        },
    ]

    df_styled.set_table_styles(styles)

    df_styled.highlight_null(
        props="background-color: rgba(255, 0, 0, 0.5); color: white;"
    )

    df_styled.hide(subset=None, level=None, names=False).to_html(output)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Generate a summary of the completed time series"
    )

    parser.add_argument(
        "--filepath-completed",
        type=str,
        help="Path of Station completed file",
        required=True,
        dest="filepath_completed",
        metavar="STRING",
    )
    parser.add_argument(
        "--filepath-replaced",
        type=str,
        help="Path of file that contains only data which have changed",
        required=True,
        dest="filepath_replaced",
        metavar="STRING",
    )
    parser.add_argument(
        "--color",
        type=str,
        help="Color of replaced data",
        default="cyan",
        dest="color",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of Station completed CSV",
        default=";",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Output file path",
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    complete_timeseries_summary(
        filepath_completed=args.filepath_completed,
        filepath_replaced=args.filepath_replaced,
        color=args.color,
        delimiter=args.delimiter,
        output=args.output+"/CompleteSeriesSummary.html",
    )
