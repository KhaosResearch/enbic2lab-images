import pandas as pd
from argparse import ArgumentParser
from functools import reduce
from IPython.display import HTML
import numpy as np
import re


# TODO --> It might be worth it to try to implement this function using the pandas Styler class


my_style = """
border-bottom-color: rgba(0, 0, 0, 0);
border-bottom-style: solid;
border-bottom-width: 2px;
border-collapse: collapse;
border-image-outset: 0px;
border-image-repeat: stretch;
border-image-slice: 100%;
border-image-source: none;
border-image-width: 1;
border-left-color: rgba(0, 0, 0, 0);
border-left-style: solid;
border-left-width: 2px;
border-right-color: rgba(0, 0, 0, 0);
border-right-style: solid;
border-right-width: 2px;
border-top-color: rgba(0, 0, 0, 0);
border-top-style: solid;
border-top-width: 2px;
box-sizing: border-box;
color: rgb(0, 0, 0);
display: table;
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size: 16px;
height: 1675px;
line-height: 20px;
margin-left: auto;
margin-right: auto;
margin-top: 12px;
table-layout: fixed;
text-size-adjust: 100%;
width: max-content;
cursor: default;
-webkit-border-horizontal-spacing: 0px;
-webkit-border-vertical-spacing: 0px;
-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"""


def styled_html(df, style=None, id=None) -> HTML:
    """Generate styled HTML representation of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be represented as HTML.
        style (str, optional): Additional CSS styles to apply (default is None).
        id (str, optional): The HTML element ID for the table (default is None).

    Returns:
        HTML: A styled HTML representation of the DataFrame.

    This function generates an HTML representation of a DataFrame with optional styling and IDs.
    """
    df_html = df.to_html(
        index=False,
        escape=False,
    )
    df_html = df_html.replace("NaN", "")

    if id is None:
        id = "id%d" % np.random.choice(np.arange(1000000))

    # Formatting of the table
    lines = df_html.split("\n")
    for i in range(0, len(lines) - 1):
        if lines[i - 1].find("tr") != -1:
            lines[i] = lines[i].replace(
                "<td>", "<td style='border-right: solid 0.2em'>"
            )
            lines[i] = lines[i].replace(
                "<th>", "<th style='border-right: solid 0.2em'>"
            )
        if lines[i + 1].find("/tr") != -1:
            lines[i] = lines[i].replace("<td>", "<td style='border-left: solid 0.2em'>")
            lines[i] = lines[i].replace("<th>", "<th style='border-left: solid 0.2em'>")
        if lines[i - 1].find("thead") != -1:
            lines[i] = lines[i].replace("tr", "tr style='border-bottom: solid 0.2em'")
        if (
            lines[i].lower().find("max") != -1
            or lines[i].lower().find("wet years") != -1
        ):
            lines[i - 1] = lines[i - 1].replace(
                "<tr>", "<tr style='border-top: solid 0.2em'>"
            )
        if lines[i].lower().find("mean * 0.85") != -1:
            lines[i - 1] = lines[i - 1].replace(
                "<tr>", "<tr style='background-color: #fffea6'>"
            )
        if lines[i].lower().find("mean * 1.15") != -1:
            lines[i - 1] = lines[i - 1].replace(
                "<tr>", "<tr style='background-color: #9ab3d4'>"
            )
        if lines[i].lower().find('class="wet-year"') != -1:
            if lines[i].lower().find("style") != -1:
                lines[i] = lines[i].replace(
                    "style='", "style='background-color: #9ab3d4; "
                )
            else:
                lines[i] = lines[i].replace(
                    "td", "td style='background-color: #9ab3d4'"
                )
        if lines[i].lower().find('class="dry-year"') != -1:
            if lines[i].lower().find("style") != -1:
                lines[i] = lines[i].replace(
                    "style='", "style='background-color: #fffea6; "
                )
            else:
                lines[i] = lines[i].replace(
                    "td", "td style='background-color: #fffea6'"
                )

    df_html = "\n".join(lines)

    # Add the style to the table
    if style is None:
        style = """
        <style>
            table#{this_id} {{color: blue}}
        </style>
        """.format(
            this_id=id
        )
    else:
        s = re.sub(r"</?style>", "", style).strip()
        table_styles = []
        for line in s.split("\n"):
            line = line.strip()
            line = re.sub(r"^", "\t", line)
            table_styles.append(line)
        style = """<style>
            table#%s {
                %s
            }
            table#%s td, th {
                text-align: center;
                border: none;
                padding-top:0.15em;
                padding-bottom:0.15em;
            }
            table#%s th {
                padding-inline: 0.5em
            }
            table#%s tr {
                background-color: #ffffff;
            }
            table#%s tr:hover {
                filter: brightness(0.85);
            }
        </style>
        """ % (
            id,
            "\n".join(table_styles),
            id,
            id,
            id,
            id,
        )

    df_html = re.sub(r"<table", r"<table id=%s " % id, df_html)

    return HTML(style + df_html)


def plot_highlight_summary(filepath: str, output: str, delimiter: str = ";") -> None:
    """Generate a styled HTML summary from precipitation data, highlighting wet and dry years.

    Parameters:
        - filepath (str): The path to the CSV file containing precipitation data.
        - output (str): The desired path and filename for the output HTML file.
        - delimiter (str, optional): The delimiter used in the CSV file. Default is ";".

    Raises:
        - ValueError: If the CSV file does not contain the required columns
        ['Hidrologic Year', 'Station', 'Sum of the Year'].

    Usage:
        - This function reads precipitation data from a CSV file, calculates summary measures,
        and generates an HTML file highlighting wet and dry years.
        - The output HTML file will be styled with CSS styles defined by the 'my_style' variable.

    Example:
        ```python
        filepath = "path/to/precipitation_data.csv"
        output_html = "path/to/output_summary.html"
        plot_highlight_summary(filepath, output_html)
        ```
    """
    # Read the CSV file
    raw_data = pd.read_csv(filepath, delimiter=delimiter, decimal=".")

    # Check if the CSV file contains the required columns
    required_columns = ["Hidrologic Year", "Station", "Sum of the Year"]
    if all(column in raw_data.columns for column in required_columns):
        raw_data = raw_data[required_columns]
    else:
        raise ValueError(
            "The CSV file does not contain the required columns ['Hidrologic Year', 'Station', 'Sum of the Year']."
        )

    # Get the list of stations
    stations = raw_data["Station"].unique()

    # Create a list of DataFrames for each station
    list_df = [
        raw_data[raw_data.iloc[:, 1] == st]
        .iloc[:, [0, 2]]
        .rename(
            columns={raw_data.columns[0]: "Hidrologic Year", raw_data.columns[2]: st}
        )
        for st in stations
    ]

    # Merge DataFrames using reduce and merge
    data = reduce(
        lambda dtf1, dtf2: pd.merge(dtf1, dtf2, on="Hidrologic Year", how="outer"),
        list_df,
    )

    data["Annual Precipitation (mm)"] = round(
        data.iloc[:, 1:].mean(axis=1, skipna=True), 1
    )

    # Calculate the maximum, mean, and minimum of each station
    list_measures = []
    list_measures.append(
        [
            f"<b>{measure}</b>"
            for measure in ["Max", "Mean", "Min", "Mean * 1.15", "Mean * 0.85"]
        ]
    )

    for col in data.columns[1:]:
        values = data[col].dropna()
        max_val = np.max(values)
        mean_val = round(np.mean(values), 1)
        min_val = np.min(values)
        mean_115 = round(1.15 * mean_val, 1)
        mean_085 = round(0.85 * mean_val, 1)

        list_measures.append([max_val, mean_val, min_val, mean_115, mean_085])

    df_measures = pd.DataFrame(list_measures).transpose()

    # Count the number of wet, medium, and dry years for each station
    df_years = pd.DataFrame(
        columns=["<b>Wet years</b>", "<b>Middle years</b>", "<b>Dry years</b>"]
    )

    for col in range(1, len(data.columns[1:]) + 1):
        wet_years = data[data[data.columns[col]] > df_measures.loc[3, col]].index
        dry_years = data[data[data.columns[col]] < df_measures.loc[4, col]].index

        for wet_year in wet_years:
            data.loc[
                wet_year, data.columns[col]
            ] = f'<span class="wet-year">{round(data.loc[wet_year, data.columns[col]], 1)}</span>'
        for dry_year in dry_years:
            data.loc[
                dry_year, data.columns[col]
            ] = f'<span class="dry-year">{round(data.loc[dry_year, data.columns[col]], 1)}</span>'

        df_years.loc[len(df_years)] = [
            len(wet_years),
            len(data[data.columns[col]].dropna()) - len(wet_years) - len(dry_years),
            len(dry_years),
        ]

    df_years = df_years.transpose()
    df_years.reset_index(inplace=True)

    # Add the information to the main data frame
    df_measures.columns = data.columns
    df_years.columns = data.columns

    # Highlight the Dry and Wet years
    dt = data[data.columns[1:]].dropna(
        axis=0,
        how="all",
    )

    for row in dt.index:
        elements = dt.loc[row].dropna().tolist()
        wets = 0
        dries = 0
        for element in elements:
            if str(element).find("wet-year") != -1:
                wets += 1
            if str(element).find("dry-year") != -1:
                dries += 1
        if wets == len(elements):
            data.iloc[row, 0] = f'<span class="wet-year">{data.iloc[row, 0]}</span>'
        if dries == len(elements):
            data.iloc[row, 0] = f'<span class="dry-year">{data.iloc[row, 0]}</span>'

    data = pd.concat([data, df_measures], ignore_index=True)
    data = pd.concat([data, df_years], ignore_index=True)

    html = styled_html(data, style=my_style)
    with open(output, "w") as f:
        f.write(html.data)


if __name__ == "__main__":
    parser = ArgumentParser(description="Writes a summary table into an HTML file.")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file.",
        required=True,
        dest="filepath",
        metavar="STRING",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file.",
        default=";",
        required=False,
        dest="delimiter",
        metavar="CHAR",
    )

    parser.add_argument(
        "--output-path",
        type=str,
        help="Path for the output HTML file.",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    plot_highlight_summary(
        filepath=args.filepath, delimiter=args.delimiter, output=args.output+"/output.html"
    )
