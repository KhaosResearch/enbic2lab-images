from re import findall
from typing import List
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder


# ======= METHODS =======
def generic_pca_plot(
    filepath: str,
    target_column: str,
    output_path: str,
    color_list: List[str] = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    delimiter: str = ",",
    
):
    """
    Generate a PCA scatter plot from data in a CSV file and save the plot in multiple formats.

    Parameters:
    - filepath (str): The path to the input CSV file containing data for PCA.
    - target_column (str): The column representing the target variable for color-coding.
    - output_path (str): The path to save the output plot files (PDF, PNG, SVG).
    - color_list (List[str], optional): List of colors for each target category. 
      If not provided, a default color palette is used. Default is None.
    - title (str, optional): The title of the plot. Default is None.
    - x_label (str, optional): The label for the x-axis. Default is None.
    - y_label (str, optional): The label for the y-axis. Default is None.
    - delimiter (str, optional): The delimiter used in the CSV file. Default is ",".

    Returns:
    None

    Usage:
    - This function reads data from a CSV file, performs PCA, and generates a scatter plot using seaborn.
      The resulting plot is saved in PDF, PNG, and SVG formats in the specified output directory.
    """

    sns.set_theme()
    
    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter)
    numeric = ["int16", "int32", "int64", "float16", "float32", "float64"]

    data.dropna(inplace=True, thresh=len(data.index)/2, axis=1) # Drop columns with more than 50% missing values
    data.dropna(inplace=True, axis=0) # Drop rows with missing values
    
    # Prepare data for PCA
    X = data.drop(target_column, axis=1)
    y = data[target_column].to_numpy()
    target_names = data[target_column].unique()

    for col in X.columns:
        if X[col].dtype not in numeric:
            X.pop(col)

    # PCA
    pca = PCA(n_components=2)
    pca_data = pca.fit(X).transform(X)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Controlling color palette
    if not color_list:
        print("No color list provided. Using default color palette 'tab10'.")
        color_list = sns.palettes.color_palette("tab10", len(target_names)).as_hex() # Default color palette    
    elif len(color_list) < len(target_names):
        print(f"Number of colors ({len(color_list)}) does not match number of target labels ({len(target_names)}). Using default color palette 'tab10'.")
        color_list = sns.palettes.color_palette("tab10", len(target_names)).as_hex() # Default color palette
    elif len(color_list) > len(target_names):
        print(f"Number of colors ({len(color_list)}) does not match number of target labels ({len(target_names)}). Using first {len(target_names)} colors.")
        color_list = color_list[:len(target_names)] # Use first n colors

    for color, target_name in zip(color_list, target_names):
        sns.scatterplot(
            x=pca_data[y == target_name, 0],
            y=pca_data[y == target_name, 1],
            color=color,
            alpha=0.8,
            label=target_name,
            linewidth=0,
            s=50,
            ax=ax,
        )
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, scatterpoints=1)
    if title and title != "":
        ax.set_title(title, fontsize=15, fontweight="bold", loc="center", pad=20)
    if x_label and x_label != "":
        ax.set_xlabel(x_label)
    if y_label and y_label != "":
        ax.set_ylabel(y_label)
    
    # Save plot
    file = f"{output_path}/pca_plot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# ======= MAIN =======
if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a PCA plot from a CSV file.")
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="File path of the CSV file",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--target-column",
        type=str,
        required=True,
        help="Name of the target column",
        dest="target_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--color-list",
        type=str,
        required=False,
        default=None,
        help="Color codes for scatter plot. One color per target label. Separate colors with commas.",
        dest="color_list",
        metavar="STRING",
    )
    parser.add_argument(
        "--title",
        type=str,
        required=False,
        default=None,
        help="Title of the plot",
        dest="title",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-label",
        type=str,
        required=False,
        default=None,
        help="Label of the x-axis",
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-label",
        type=str,
        required=False,
        default=None,
        help="Label of the y-axis",
        dest="y_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the CSV file",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path of the plot",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    args.color_list = findall(r'\s*([^,]+)\s*', args.color_list) if args.color_list != None else None

    generic_pca_plot(
        filepath=args.filepath,
        delimiter=args.delimiter,
        color_list=args.color_list,
        target_column=args.target_column,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        output_path=args.output,
    )
    
