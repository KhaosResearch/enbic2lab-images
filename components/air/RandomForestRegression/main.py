import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from pathlib import Path
import math
import argparse

def main(filepath:str,output:str,dependent_variable:str="Olea", date_column: str="Date", delimiter: str = ";") -> None:
    """
    Random forest regresion
    """
    df = pd.read_csv(filepath, sep=delimiter, index_col=date_column)
    df.dropna(inplace=True)
    X = df.drop(dependent_variable, axis=1).to_numpy()
    y = df[dependent_variable].to_numpy()
    r2_list=[]
    mae_list=[]
    rmse_list=[]
    rmse_mae_list=[]


    tscv = TimeSeriesSplit()
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        reg = RandomForestRegressor().fit(X_train, y_train)
        y_predict = reg.predict(X_test)
        r2 = r2_score(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = math.sqrt(mean_squared_error(y_test, y_predict))
        if mae != 0:       
            rmse_mae = rmse / mae
        else:
            rmse_mae = rmse
        r2_list.append(r2)
        mae_list.append(mae)
        rmse_list.append(rmse)
        rmse_mae_list.append(rmse_mae)
    r2_mean = np.mean(r2_list)
    mae_mean = np.mean(mae_list)
    rmse_mean = np.mean(rmse_list)
    rmse_mae_mean = np.mean(rmse_mae_list)
    final_df = pd.DataFrame({
        'r2_mean': [r2_mean],
        'mae_mean': [mae_mean],
        'rmse_mean': [rmse_mean],
        'rmse_mae_mean': [rmse_mae_mean]
    })
    print(final_df)
    final_df.to_csv(output, sep=delimiter, index=None)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a CSV file to JSON.")
    
    parser.add_argument(
        "--filepath",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
        default="/mnt/shared/input.csv",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        required=False,
        help="Name of date column",
        default="Date",
    )
    parser.add_argument(
        "--dependent-variable",
        type=str,
        required=False,
        help="Dependent variable",
        default="Olea",
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
        args.filepath,
        args.output,
        args.dependent_variable,
        args.date_column,
        args.delimiter
    )
