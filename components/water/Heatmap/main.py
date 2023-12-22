import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from argparse import ArgumentParser


def heatmap(
    filepath: str,
    percentage_column: str,
    output: str,
    date_column: str = "Hidrologic Year",
    station_column: str = "Station",
    delimiter: str = ";",
    palette: str = "RdYlBu_r",
) -> None:
    """Create a heatmap from precipitation data.

    This function reads a CSV file containing precipitation data, generates a heatmap
    visualizing the data, and saves it as an image file.

    Args:
        filepath (str): The path to the CSV file containing precipitation data.
        date_column (str): The name of the column containing dates (default is "Hidrologic Year").
        station_column (str): The name of the column containing station names (default is "Station").
        percentage_column (str): The name of the column containing the percentage of
            collected data (used for color gradient in the heatmap).
        output (str): The path to save the generated heatmap image.
        delimiter (str, optional): The delimiter used in the CSV file (default is ";").
        palette (str, optional): The color palette for the heatmap (default is "RdYlBu_r"). Available options:
    
    Raises:
        OverflowError: If the resulting heatmap is too big to be generated.

    Returns:
        None

    This function generates a heatmap, customizing its appearance and saving it as an
    image file. The resulting heatmap provides insights into precipitation data for
    different stations over time.

    Note:
        Available color maps include:
            - 'rocket'
            - 'mako'
            - 'flare'
            - 'crest'
            - 'rocket_r'
            - 'mako_r'
            - 'flare_r'
            - 'crest_r'
            - 'viridis'
            - 'plasma'
            - 'inferno'
            - 'magma'
            - 'cividis'
            - 'viridis_r'
            - 'plasma_r'
            - 'inferno_r'
            - 'magma_r'
            - 'cividis_r'
            - 'Greys'
            - 'Reds'
            - 'Greens'
            - 'Blues'
            - 'Oranges'
            - 'Purples'
            - 'BuGn'
            - 'BuPu'
            - 'GnBu'
            - 'OrRd'
            - 'PuBu'
            - 'PuRd'
            - 'RdPu'
            - 'YlGn'
            - 'PuBuGn'
            - 'YlGnBu'
            - 'YlOrBr'
            - 'YlOrRd'
            - 'Greys_r'
            - 'Reds_r'
            - 'Greens_r'
            - 'Blues_r'
            - 'Oranges_r'
            - 'Purples_r'
            - 'BuGn_r'
            - 'BuPu_r'
            - 'GnBu_r'
            - 'OrRd_r'
            - 'PuBu_r'
            - 'PuRd_r'
            - 'RdPu_r'
            - 'YlGn_r'
            - 'PuBuGn_r'
            - 'YlGnBu_r'
            - 'YlOrBr_r'
            - 'YlOrRd_r'
            - 'Greys_d'
            - 'Reds_d'
            - 'Greens_d'
            - 'Blues_d'
            - 'Oranges_d'
            - 'Purples_d'
            - 'BuGn_d'
            - 'BuPu_d'
            - 'GnBu_d'
            - 'OrRd_d'
            - 'PuBu_d'
            - 'PuRd_d'
            - 'RdPu_d'
            - 'YlGn_d'
            - 'PuBuGn_d'
            - 'YlGnBu_d'
            - 'YlOrBr_d'
            - 'YlOrRd_d'
            - 'vlag'
            - 'vlag_r'
            - 'icefire'
            - 'icefire_r'
            - 'coolwarm'
            - 'bwr'
            - 'sismic'
            - 'RdBu'
            - 'RdGy'
            - 'PRGn'
            - 'PiYG'
            - 'BrBG'
            - 'RdYlBu'
            - 'RdYlGn'
            - 'Spectral'
            - 'RdBu_r'
            - 'RdGy_r'
            - 'PRGn_r'
            - 'PiYG_r'
            - 'BrBG_r'
            - 'RdYlBu_r'
            - 'RdYlGn_r'
            - 'Spectral_r'
    """
    data = pd.read_csv(filepath, sep=delimiter, decimal=".")

    result = data.pivot(
        index=date_column, columns=station_column, values=percentage_column
    )
    labels = result.round(1).values

    sorted_stations = sorted(result.columns.values, key=len, reverse=True)
    longest_word = len(sorted_stations[0])

    fig, ax = plt.subplots(
        figsize=(
            longest_word * len(sorted_stations) * (0.39370079 / 2),
            result.shape[0] * 0.75,
        ),
        dpi=300
    )
    title = "Heatmap"
    plt.title(title, fontsize=5 * (result.shape[0] ** 0.5), y=1.02)
    ax.xaxis.tick_top()

    if(result.shape[0]*result.shape[1] > 3750):
        raise OverflowError("Data size is too big. Try reducing the number of stations or dates.")

    h = sns.heatmap(
        result,
        annot=labels,
        fmt="",
        cmap=palette,
        linewidth=0.50,
        ax=ax,
        cbar_kws={"label": "Collected Data (%)"},
        center=50,
        annot_kws={"size": 2 * (result.shape[0] ** 0.5)},
    )
    h.set_xlabel(h.get_xlabel(), size=3 * (result.shape[0] ** 0.5))
    h.set_ylabel(h.get_ylabel(), size=3 * (result.shape[0] ** 0.5))

    cbar = h.collections[0].colorbar
    cbar.ax.tick_params(labelsize=2.2 * (result.shape[0] ** 0.5))
    cbar.ax.set_ylabel(cbar.ax.get_ylabel(), size=2.75 * (result.shape[0] ** 0.5))

    fig.savefig(output, dpi=300, format="png", bbox_inches="tight")


if __name__ == "__main__":
    parser = ArgumentParser(description="Create a heatmap from precipitation data")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Name of the csv file",
        required=True,
        metavar="STRING",
        dest="filepath",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        help="The name of the date's column",
        required=False,
        default="Hidrologic Year",
        metavar="STRING",
        dest="date_column",
    )
    parser.add_argument(
        "--station-column",
        type=str,
        help="The name of the station's column",
        required=False,
        default="Station",
        metavar="STRING",
        dest="station_column",
    )
    parser.add_argument(
        "--percentage-column",
        type=str,
        help="The name of the Percentage of Collected Data's column (Color Gradient's Heatmap)",
        required=True,
        metavar="STRING",
        dest="percentage_column",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the csv file",
        required=False,
        default=";",
        metavar="STRING",
        dest="delimiter",
    )
    parser.add_argument(
        "--palette",
        type=str,
        help="Color Palette. See: https://seaborn.pydata.org/tutorial/color_palettes.html#palette-tutorial",
        required=False,
        default="RdYlBu_r",
        metavar="STRING",
        dest="palette",
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
        "--output-path",
        type=str,
        help="Path to save the generated heatmap image",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    heatmap(
        filepath=args.filepath,
        delimiter=args.delimiter,
        date_column=args.date_column,
        station_column=args.station_column,
        percentage_column=args.percentage_column,
        palette=args.palette,
        output=args.output+"/water_heatmap.png",
    )
