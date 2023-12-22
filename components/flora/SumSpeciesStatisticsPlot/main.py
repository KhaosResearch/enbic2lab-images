import argparse
import matplotlib.pyplot as plt
import pandas as pd

def main(
    filepath: str,
    delimiter: str,
    n_samples: int,
    color_plot: str,
    output: str,
) -> None:
    """
    Generate a bar plot of the top n_samples species from a CSV file.

    Args:
        filepath (str): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file.
        n_samples (int): Number of samples to plot.
        color_plot (str): Color of the bar plot.
        output (str): Path to save the plot.
    """
    # Read the CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Calculate the percentage of each species
    data["Sum_Species_Percentage"] = data["Sum_Species"] / data["Sum_Species"].sum()

    # Sort the data by the percentage of species in descending order
    data = data.sort_values(by=["Sum_Species_Percentage"], ascending=False)

    # Get the top n_samples data
    data2 = data.head(n_samples)

    # Get the labels and sizes for plotting
    labels = data2["Species"].values
    sizes = data2["Sum_Species"]

    # Create the bar plot
    fig, ax = plt.subplots()
    ax.yaxis.grid()
    ax.set_axisbelow(True)
    ax.bar(labels, sizes, align="center", color=color_plot)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Sum of Species")
    ax.set_title(f"Sum of Species top {n_samples}")
    plt.xticks(rotation=90)

    # Save the plot to the output file
    fig.savefig(output, bbox_inches="tight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the top n species of the input CSV File")

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
        required=True,
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
        args.output+"/output.pdf",
    )
