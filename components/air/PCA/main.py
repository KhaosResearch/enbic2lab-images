import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.decomposition import PCA
import argparse


def pca_analysis(filepath: str, delimiter: str, pollen_type: str, date_column: str, output: str, n_components:float = 0.7):
    """
    Given a pandas dataset perform a PCA analysis to select the most important features
    """
    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col=date_column)
    
    X = dataframe.values
    sc = StandardScaler()
    X_std = sc.fit_transform(X)
    pca = PCA(n_components=n_components, svd_solver="full")
    pca.fit(X_std)
    n_pcs = pca.n_components_
    
    # get the index of the most important feature on EACH component
    most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]
    initial_feature_names = dataframe.columns
    
    # get the most important feature names
    most_important_names = [
        initial_feature_names[most_important[i]] for i in range(n_pcs)
    ]
    
    most_important_names.append(pollen_type)
    cols = sorted(list(set(most_important_names)))
    dataframe[cols].to_csv(output, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCA Analysis component")
    parser.add_argument(
        "--filepath",
        type=str,
        default="lagged_time_series.csv",
        help="Input CSV file path.",
    )
    parser.add_argument("--delimiter", type=str, default=";", help="Delimiter used in CSV.")
    parser.add_argument("--pollen-column", type=str, help="Name of pollen column")
    parser.add_argument("--date-column", type=str, default="date", help="Name of date column")
    parser.add_argument("--n-components", type=float, default=0.7, help="N components")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/pca.csv",
        help="Output path.",
    )

    args = parser.parse_args()

    pca_analysis(args.filepath, args.delimiter, args.pollen_column, args.date_column, args.output, args.n_components)
