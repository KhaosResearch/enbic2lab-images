import argparse
import csv
from typing import List, Tuple

import matplotlib.pyplot as plt


def read_csv(filepath: str, delimiter: str) -> Tuple[List[str], List[float], List[float]]:
    """Read data from a CSV file."""
    labels, min_altitude, max_altitude = [], [], []

    try:
        with open(filepath) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                labels.append(row["Community"])
                min_altitude.append(float(row["Min_Alt"]))
                max_altitude.append(float(row["Max_Alt"]))
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return [], [], []
    except KeyError:
        print("Invalid column name in CSV.")
        return [], [], []

    return labels, min_altitude, max_altitude


def plot_data(labels: List[str], min_altitude: List[float], max_altitude: List[float], output: str) -> None:
    """Plot data using matplotlib."""
    if len(labels) == 0:
        print("No data found.")
        return

    # Figure size depends on the number of communities,
    # so that the plot is not too crowded.
    pixelsize = 0.8
    figsize = (pixelsize * len(labels), 8)
    fig, ax = plt.subplots(figsize=figsize)

    plt.grid()
    ax.bar(labels, max_altitude, bottom=min_altitude, align="center")
    ax.set_axisbelow(True)
    ax.set_title("Community Altitude Range")
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Altitude Range (m)")
    ax.margins(x=0)
    plt.xticks(rotation=90)

    fig.savefig(output, format="pdf", bbox_inches="tight")


def main(filepath: str, delimiter: str, output: str) -> None:
    labels, min_altitude, max_altitude = read_csv(filepath, delimiter)
    plot_data(labels, min_altitude, max_altitude, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the altitude range of each community.")
    parser.add_argument(
        "--filepath",
        type=str,
        default="community_altitude_range.csv",
        help="Input CSV file path.",
    )
    parser.add_argument("--delimiter", type=str, default=";", help="Delimiter used in CSV.")
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )
    args = parser.parse_args()

    main(args.filepath, args.delimiter, args.output+"/output.pdf")
