import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main(
    filepath: str, delimiter: str, n_samples: int, color_plot: str, output: str
) -> None:
    """
    Generate a bar plot of mean coverage for the top n samples of a given dataset.

    Args:
        filepath (str): The path to the CSV file containing the dataset.
        delimiter (str): The delimiter used in the CSV file.
        n_samples (int): The number of top samples to consider.
        color_plot (str): The color of the bars in the plot.
        output (str): The file path to save the plot.

    Returns:
        None
    """
    # Read the dataset from the CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Sort the dataset by "Mean Coverage" column in ascending order
    data = data.sort_values(by="Mean Coverage", axis=0, ascending=True)

    # Select the top n samples from the dataset
    data = data.head(n_samples)

    # Extract the x and y values for the bar plot
    x = data["Community"]
    y = data["Mean Coverage"]

    # Create a bar plot with error bars
    fig, ax = plt.subplots()
    ax.yaxis.grid()
    ax.set_axisbelow(True)
    ax.bar(
        x,
        y,
        align="center",
        yerr=data["Mean Coverage Standard Error"],
        alpha=1,
        ecolor="black",
        capsize=2,
        color=color_plot,
    )
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Mean coverage (%)")
    ax.set_title(f"Community Mean Coverage top {n_samples}")
    plt.xticks(rotation=90)

    # Save the plot to the specified output file
    fig.savefig(output, bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot the Mean Coverage per community from a CSV File"
    )

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath of the CSV file",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=True,
        help="Delimiter of the CSV file",
    )

    parser.add_argument(
        "--n-samples",
        type=int,
        default=10,
        help="Number of samples that will appear in the plot",
    )

    parser.add_argument(
        "--color-plot",
        type=str,
        default="#006400",
        help="Hexadecimal code for color plot",
    )
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

    main(
        args.filepath,
        args.delimiter,
        args.n_samples,
        args.color_plot,
        args.output + "/output.pdf",
    )
