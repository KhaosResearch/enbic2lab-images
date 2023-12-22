import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from argparse import ArgumentParser


def __dimension_reduction(percentage_variance: list, variance_explained: int = 75):
    """Calculate the number of components required to achieve a specified percentage of explained variance.

    This private helper function calculates the number of principal components needed to achieve a desired percentage of explained variance in a PCA analysis.

    Args:
        - percentage_variance (list): A list of percentages of explained variance for each component.
        - variance_explained (int): The target percentage of variance to be explained. The default is 75.

    Returns:
        - n_components (int): The number of principal components required to achieve the specified percentage of explained variance.

    Note:
        This function is used internally by the `pca_soil` function.
    """

    cumulative_variance = 0
    n_components = 0
    while cumulative_variance < variance_explained:
        cumulative_variance += percentage_variance[n_components]
        n_components += 1
    return n_components


def pca_soil(
    filepath: str,
    delimiter: str,
    output_corr_matrix: str,
    output_scree_plot: str,
    output_pca_plot: str,
    output_cov_matrix: str,
    number_components: int = None,
    variance_explained: int = 75,
    target_column: str = None,
):
    """
    Perform Principal Component Analysis (PCA) on soil data from a CSV file with options for specifying the number of components or explained variance.

    This function reads soil data from a CSV file, performs PCA, and saves various output files, including the correlation matrix heatmap, scree plot, PCA plot, and covariance matrix. It allows you to specify the number of components or the desired percentage of explained variance.

    Args:
        - filepath (str): The path to the CSV file containing soil data for PCA analysis.
        - delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        - output_corr_matrix (str): The path to save the correlation matrix heatmap as a CSV file.
        - output_scree_plot (str): The path to save the scree plot showing the explained variance as a CSV file.
        - output_pca_plot (str): The path to save the PCA plot data as a CSV file.
        - output_cov_matrix (str): The path to save the covariance matrix as a CSV file.
        - number_components (int): Number of components desired after dimension reduction. If not specified or an invalid value is provided, the number of components will be calculated based on variance_explained. Default is None.
        - variance_explained (int): The target percentage of variance to be explained by the Principal Components. Default is None.
        - target_column (str): The name of the column containing the target variable. Default is None.

    Raises:
        - ValueError: If the provided CSV file is not in a valid format or cannot be read.

    Example:
        To perform PCA on soil data in a CSV file 'soil_data.csv' using a semicolon (';') as the delimiter, specify 3 as the number of components, and save the output files to specified locations:

        >>> pca_soil(
                filepath="soil_data.csv",
                delimiter=";",
                output_corr_matrix="/path/to/correlation_matrix.csv",
                output_scree_plot="/path/to/scree_plot.csv",
                output_pca_plot="/path/to/pca_plot.csv",
                output_cov_matrix="/path/to/covariance_matrix.csv",
                number_components=3
                target_column="target"
            )

    Note:
        - The correlation matrix heatmap is saved as 'output_corr_matrix'.
        - The scree plot is saved as 'output_scree_plot'.
        - The PCA plot data is saved as 'output_pca_plot'.
        - The covariance matrix is saved as 'output_cov_matrix'.
    """

    data = pd.read_csv(filepath, sep=delimiter, decimal=".")

    if target_column is not None:
        y_target = data[[target_column]]
        data = data.drop([target_column], axis=1)


    corr = data.corr().round(2)
    corr.to_csv(output_corr_matrix, sep=delimiter)

    pca2 = PCA()
    pca2.fit_transform(data)
    per_var = np.round(pca2.explained_variance_ratio_ * 100, decimals=1)
    np.savetxt(output_scree_plot, per_var, delimiter=delimiter)

    # If number_components is present AND is greater than 0 AND lower than the total number of columns, that value is used
    # If number_components is present AND is lower than 0, the value is calculated using variance_explained
    # If number_components is present AND is equal to 0, the value is calculated using variance_explained
    # If number_components is not present, the value is calculated using variance_explained
    # If number_components is not present OR is not valid AND variance_explained is not present, the value is calculated with a default variance_explained of 75

    # Variance is a percentage so it must be between 0 and 100

    if variance_explained is not None:
        if int(variance_explained) >= 100 or int(variance_explained) <= 0:
            variance_explained = None

    if number_components is None:
        if variance_explained is None:
            number_components = __dimension_reduction(per_var)
        else:
            number_components = __dimension_reduction(per_var, int(variance_explained))
    elif int(number_components) <= 0 or int(number_components) > len(
        data.columns.tolist()
    ):
        if variance_explained is None:
            number_components = __dimension_reduction(per_var)
        else:
            number_components = __dimension_reduction(per_var, int(variance_explained))
    else:
        number_components = int(number_components)

    pca = PCA(n_components=number_components)

    pca_data = pca.fit_transform(data)

    pc_labels = ["PC" + str(x) for x in range(1, number_components + 1)]

    pca_df = pd.DataFrame(data=pca_data, columns=pc_labels)

    if target_column is not None:
        pca_df = pd.concat([pca_df, y_target], axis=1)

    pca_df.to_csv(output_pca_plot, sep=delimiter, index=False)

    loadings = pd.DataFrame(pca.components_.T, columns=pc_labels, index=data.columns)
    loadings.to_csv(output_cov_matrix, sep=delimiter, index=True)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Perform Principal Component Analysis (PCA) on data from a CSV file, defining the number of components or the explained variance"
    )

    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file containing the data for PCA analysis",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--number-components",
        type=int,
        default=None,
        help="Number of components desired after the dimension reduction. If empty or value not valid, the number of components will be calculated using variance-explained. [default: None]",
        required=False,
        metavar="INT",
        dest="number_components",
    )
    parser.add_argument(
        "--variance-explained",
        type=int,
        default=75,
        help="The total variace that is wanted to be explained by the Principal Components. Variance is a percentege value. If empty the number of components will be calculated using a default value of 75. [default: 75]",
        required=False,
        metavar="INT",
        dest="variance_explained",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        help="Delimiter used in the CSV file to separate values [default: ';']",
        required=False,
        metavar="CHAR",
    )
    parser.add_argument(
        "--target-column",
        type=str,
        default=None,
        help="Name of the column containing the target variable. [default: None]",
        required=False,
        metavar="STRING",
        dest="target_column",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="/mnt/shared",
        help="Path to save the output CSV files",
        required=False,
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    pca_soil(
        filepath=args.filepath,
        number_components=args.number_components,
        variance_explained=args.variance_explained,
        delimiter=args.delimiter,
        target_column=args.target_column,
        output_cov_matrix=args.output+"/covariance_matrix.csv",
        output_corr_matrix=args.output+"/correlation_matrix_heatmap.csv",
        output_pca_plot=args.output+"/PCA_plot.csv",
        output_scree_plot=args.output+"/scree_plot.csv",
    )
