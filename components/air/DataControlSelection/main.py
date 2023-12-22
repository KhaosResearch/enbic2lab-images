import argparse
import pandas as pd

def main(filepath_metrics:str,filepath_pandas:str,filepath_mean:str, output: str, delimiter: str = ";") -> None:
    """
    Select the best CSV by metrics comparation.
    """

    df = pd.read_csv(filepath_metrics, delimiter=delimiter)
    best_file = ""
    best_r2_ = df['r2_mean'].idxmax()
    best_mae_mean = df['mae_mean'].idxmin()
    best_rmse_mean = df['rmse_mean'].idxmin()
    best_rmse_mae_mean = df['rmse_mae_mean'].idxmin()

    list_best = [best_r2_,best_mae_mean,best_rmse_mean,best_rmse_mae_mean]
    dict_ocurrence = dict()
    for index, row in df.iterrows():
        dict_ocurrence[index] = list_best.count(index)

    ocurrence_values = list(dict_ocurrence.values())
    max_ocurrence = max(ocurrence_values)
    count_max_ocurrence = ocurrence_values.count(max_ocurrence)

    if count_max_ocurrence == 1: 
        indx = ocurrence_values.index(max_ocurrence)
        best_file = "/mnt/shared/"+ df['filename'].iloc[indx] 
    else: 
        max_r2 = 0
        for elem in dict_ocurrence:
            if dict_ocurrence[elem] == max_ocurrence:
                if df['r2_mean'].iloc[elem] > max_r2:
                    max_r2 = df['r2_mean'].iloc[elem]
                    best_file ="/mnt/shared/"+ df['filename'].iloc[elem] 
    print(best_file)
    if best_file == filepath_pandas:
        df_final = pd.read_csv(filepath_pandas, sep=delimiter)
    elif best_file == filepath_mean:
        df_final = pd.read_csv(filepath_mean, sep=delimiter)

    df_final.to_csv(output, sep=delimiter, index=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a CSV file to JSON.")
    
    parser.add_argument(
        "--filepath-metrics",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
    )
    parser.add_argument(
        "--filepath-pandas",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
    )
    parser.add_argument(
        "--filepath-mean",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter of the CSV file",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Filepath of the output HTML file",
        default="/mnt/shared/output.csv"
    )
    
    args = parser.parse_args()

    main(
        args.filepath_metrics,
        args.filepath_pandas,
        args.filepath_mean,
        args.output,
        args.delimiter
    )
