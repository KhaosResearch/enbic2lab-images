import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from argparse import ArgumentParser


def clustermap(
    filepath: str,
    delimiter: str,
    square_column: str,
    output: str,
    date_column: str = "Hidrologic Year",
    station_column: str = "Station",
    palette: str = "PuBu",
    filter_row: bool = True,
    drop_na: bool = False,
):
    """
    Generate a cluster map from hydrological data.

    This function reads a CSV file containing hydrological data, reshapes it into a
    pivot table, and generates a cluster map to visualize the relationships between
    hydrological years and stations.

    Args:
        filepath (str): The path to the CSV file containing hydrological data.
        delimiter (str): The delimiter used in the CSV file.
        square_column (str): The name of the column containing data for the cluster map.
        output (str): The path to save the generated cluster map image.
        date_column (str, optional): The name of the column containing hydrological years
            (default is "Hidrologic Year").
        station_column (str, optional): The name of the column containing station names
            (default is "Station").
        palette (str, optional): The color palette for the cluster map (default is "PuBu").
        filter_row (bool, optional): If True, the distance computation will be based on
            rows; if False, it will be based on columns (default is True).
        drop_na (bool, optional): If True, rows and columns with all NaN values will be
            dropped; if False, NaN values will be replaced with column means
            (default is False).

    Returns:
        None
    """
    df = pd.read_csv(filepath, sep=delimiter, decimal=".")

    # Either 0 (rows) or 1 (columns) to choose which dimension of the dataset will be used to compute distances.
    filter = 0 if filter_row else 1

    df_reshaped = df.pivot(
        index=date_column, columns=station_column, values=square_column
    )

    # If drop_na remove all rows with NaN values, else replace NaN values with the mean of the column
    if not drop_na:
        df_mean = df_reshaped.mean()
        df_reshaped = df_reshaped.fillna(df_mean)
    else:
        df_reshaped = df_reshaped.dropna(axis=0, how="any")

    # Drop columns with all NaN values
    df_reshaped = df_reshaped.dropna(axis=1, how="all")
    df_reshaped = df_reshaped.dropna(axis=0, how="all")

    n_rows = len(df_reshaped.index)

    try:
        # WARNING: When using the filter by columns sometimes it fails.
        # Uses Euclidean distance and Average method to do the clustering by default.
        cluster_map = sns.clustermap(
            df_reshaped,
            standard_scale=filter,
            cmap=palette,
            figsize=(10, n_rows * 0.275),
            dendrogram_ratio=(0.15, 0.05),
            linewidth=0.05,
            cbar_pos=(0.05, 0, 0.3, 0.01),
            cbar_kws={"label": square_column, "orientation": "horizontal"},
        )
        cluster_map.fig.suptitle("Sum of the hydrological year", y=1)

        cluster_map.savefig(output, bbox_inches="tight", format="png", dpi=300)
    except ValueError:
        raise ValueError(
            "Error when calculating the clustermap. Try using a smaller dataset or changing the filter type"
        )


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a clustermap")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Name of the csv file",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--square-column",
        type=str,
        help=f"The name of the statistic to compare. For Precipitation: 'Sum of the Year'. For Temperature: 'Year Mean'."
        "Two different ways: "
        "Precipitation: Sum of the Year. "
        "Temperature: Year Mean",
        required=True,
        metavar="STRING",
        dest="square_column",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="[default value: ';']Delimiter of the csv file",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        help="[default value: 'Hidrologic Year'] The name of the date's column",
        required=False,
        default="Hidrologic Year",
        metavar="STRING",
        dest="date_column",
    )
    parser.add_argument(
        "--station-column",
        type=str,
        help="[default value: 'station_column'] The name of the station's column",
        required=False,
        default="Station",
        metavar="STRING",
        dest="station_column",
    )
    parser.add_argument(
        "--palette",
        type=str,
        help="[Default value: PuBu] Color Palette. See: https://seaborn.pydata.org/tutorial/color_palettes.html#palette-tutorial",
        required=False,
        default="PuBu",
        metavar="STRING",
        choices=[
            "rocket",
            "mako",
            "flare",
            "crest",
            "rocket_r",
            "mako_r",
            "flare_r",
            "crest_r",
            "viridis",
            "plasma",
            "inferno",
            "magma",
            "cividis",
            "viridis_r",
            "plasma_r",
            "inferno_r",
            "magma_r",
            "cividis_r",
            "Greys",
            "Reds",
            "Greens",
            "Blues",
            "Oranges",
            "Purples",
            "BuGn",
            "BuPu",
            "GnBu",
            "OrRd",
            "PuBu",
            "PuRd",
            "RdPu",
            "YlGn",
            "PuBuGn",
            "YlGnBu",
            "YlOrBr",
            "YlOrRd",
            "Greys_r",
            "Reds_r",
            "Greens_r",
            "Blues_r",
            "Oranges_r",
            "Purples_r",
            "BuGn_r",
            "BuPu_r",
            "GnBu_r",
            "OrRd_r",
            "PuBu_r",
            "PuRd_r",
            "RdPu_r",
            "YlGn_r",
            "PuBuGn_r",
            "YlGnBu_r",
            "YlOrBr_r",
            "YlOrRd_r",
            "Greys_d",
            "Reds_d",
            "Greens_d",
            "Blues_d",
            "Oranges_d",
            "Purples_d",
            "BuGn_d",
            "BuPu_d",
            "GnBu_d",
            "OrRd_d",
            "PuBu_d",
            "PuRd_d",
            "RdPu_d",
            "YlGn_d",
            "PuBuGn_d",
            "YlGnBu_d",
            "YlOrBr_d",
            "YlOrRd_d",
            "vlag",
            "vlag_r",
            "icefire",
            "icefire_r",
            "coolwarm",
            "bwr",
            "sismic",
            "RdBu",
            "RdGy",
            "PRGn",
            "PiYG",
            "BrBG",
            "RdYlBu",
            "RdYlGn",
            "Spectral",
            "RdBu_r",
            "RdGy_r",
            "PRGn_r",
            "PiYG_r",
            "BrBG_r",
            "RdYlBu_r",
            "RdYlGn_r",
            "Spectral_r",
        ],
    )

    parser.add_argument(
        "--filter-row",
        dest="filter_row",
        type=str.lower,
        help="[default value: Rows] Filter the clustermap by row, if False filter by columns",
        required=False,
        default="Rows",
        metavar="BOOLEAN",
        choices=[
            "rows",
            "columns",
            "row",
            "column"
        ],
    )

    parser.add_argument(
        "--drop-na",
        dest="drop_na",
        type=str.lower,
        help="[default value: False (mean)]If present rows with NaN values will be removed, else NaN values will be replaced with the mean of the column",
        required=False,
        default="False",
        metavar="BOOLEAN",
        choices=[
            "true",
            "false",
            "1",
            "0",
            "yes",
            "no",
            "t",
            "f"
        ],
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared] The path to save the generated cluster map image",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    # Convert filter_row argument to boolean
    if args.filter_row in ["rows", "row", "Rows", "Row", "r", "R"]:
        args.filter_row = True
    else:
        args.filter_row = False

    
    # Convert drop_na argument to boolean
    if args.drop_na in ["True", "true", "TRUE", "1", "yes", "Yes", "YES", "T", "t"]:
        args.drop_na = True
    else:
        args.drop_na = False

    clustermap(
        filepath=args.filepath,
        delimiter=args.delimiter,
        date_column=args.date_column,
        station_column=args.station_column,
        square_column=args.square_column,
        palette=args.palette,
        filter_row=args.filter_row,
        drop_na=args.drop_na,
        output=args.output+"/clustermap.png",
    )
