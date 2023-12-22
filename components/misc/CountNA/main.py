from argparse import ArgumentParser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def count_na(filepath: str, output: str, delimiter: str = ";") -> None:
    """Generates pie charts to visualize the distribution of missing data in a CSV file.

    This function reads a CSV file, counts the missing (NaN) values in each column, and generates pie charts to visualize the distribution of missing data for each column. The pie charts are saved in a PDF file.

    Args:
        filepath (str): The path to the CSV file to analyze.
        output (str): The path to the output PDF file where the pie charts will be saved.
        delimiter (str, optional): The delimiter used in the CSV file. Default is ';'.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        pd.errors.ParserError: If there is an error parsing the CSV file.

    Note:
        - This function generates a separate pie chart for each column in the CSV file, illustrating the proportion of collected data and missing data (NaN values).
        - The pie charts are saved in a PDF file with one chart per page, and each chart is labeled with the column name.
    """

    try:
        df = pd.read_csv(filepath, sep=delimiter)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{filepath}' not found.")

    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"Error: Failed to parse the CSV file.")

    def generate_pie_chart(data, title, output):
        count_na = data.isna().sum()
        count_total = len(data) - count_na

        def func(pct, allvals):
            absolute = int(pct / 100.0 * np.sum(allvals))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        fig, ax = plt.subplots()
        wedges, _, _ = ax.pie(
            [count_total, count_na],
            explode=(0.05, 0.05),
            colors=["#66b3ff", "#ff9999"],
            autopct=lambda pct: func(pct, [count_total, count_na]),
            startangle=90,
        )
        ax.legend(
            wedges,
            ["Collected data", "NAs"],
            loc="lower left",
            bbox_to_anchor=(0.8, 0.7),
        )
        ax.set_title(title, fontweight="bold")
        ax.axis("equal")

        output.savefig(fig)

    with PdfPages(output) as pdf:
        for col_name in df.columns[1:]:
            generate_pie_chart(df[col_name], col_name, pdf)


if __name__ == "__main__":
    parser = ArgumentParser(description="Count NAs in a CSV file.")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file.",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter used in the CSV file.",
        default=";",
        required=False,
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to the output PDF file.",
        default="/mnt/shared",
        required=False,
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    count_na(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output=args.output+"/output.pdf",
    )
