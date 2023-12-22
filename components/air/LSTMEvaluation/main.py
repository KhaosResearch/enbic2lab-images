import math
from pathlib import Path
import argparse
import tensorflow as tf
import pandas as pd
from numpy import load, ndarray, savetxt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def compute_metrics(test: ndarray, pred: ndarray) -> dict:
    """
    Provided the forecasted and test data, computes several metrics.

    Returns a dictionary of metrics
    """
    mae_lstm = mean_absolute_error(test, pred)
    rmse_lstm = math.sqrt(mean_squared_error(test, pred))
    r2_lstm = r2_score(test, pred)

    return {"MAE": mae_lstm, "RMSE": rmse_lstm, "R2 Score": r2_lstm}


def main(
    filepath_X: str,
    filepath_Y: str,
    filepath_model: str,
    filepath_og_target: str,
    output: str,
    delimiter: str = ";",
):
    """
    Given X_test, y_test and the trained model, make predictions and evaluate the model

    Returns the model' metrics and predictions
    """
    # Load X_test and y_test array from CSV
    X_test = load(filepath_X)
    y_test = load(filepath_Y)

    # Load Best model
    best_model = tf.keras.models.load_model(filepath_model)

    # Re train the scaler
    og_target = pd.read_csv(filepath_og_target, sep=delimiter, decimal=".", header=0)
    scaler_target = MinMaxScaler()
    scaler_target.fit(og_target)

    # MAKE PREDICTIONS
    y_hat = best_model.predict(X_test)
    test = pd.DataFrame(y_test[:, -1]).values
    pred = pd.DataFrame(y_hat[:, -1, 0]).values

    test_inv = scaler_target.inverse_transform(test)
    test_inv = np.squeeze(test_inv)

    pred_inv = scaler_target.inverse_transform(pred)
    pred_inv = np.squeeze(pred_inv)

    # CALCULATE METRICS
    metrics = compute_metrics(test_inv, pred_inv)

    # Save metrics and predictions
    suffix = ".csv"

    # Save metrics in dataframe CSV
    df_metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
    path = Path(output, "lstm_metrics").with_suffix(suffix)
    df_metrics.to_csv(path, sep=delimiter)

    # Save predictions numpy array as CSV
    suffix = ".csv"
    path_predictions = Path(output, "lstm_predictions").with_suffix(suffix)
    savetxt(path_predictions, pred_inv, delimiter=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima model")

    # Define command-line arguments
    parser.add_argument(
        "--filepath-x",
        type=str,
        default="/mnt/shared/lstm_X_test.npy",
        required=True,
        help="File path of X_test csv file",
    )
    parser.add_argument(
        "--filepath-y",
        type=str,
        default="/mnt/shared/lstm_Y_test.npy",
        required=True,
        help="File path of Y_test csv file",
    )
    parser.add_argument(
        "--filepath-model",
        type=str,
        default="/mnt/shared/lstm_model.h5",
        required=True,
        help="File path of the model",
    )
    parser.add_argument(
        "--filepath-original-y",
        type=str,
        default="/mnt/shared/target.csv",
        required=True,
        help="File path of the original target dataset to be used for the scaler",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        required=False,
        help="Path to the outputs files",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=False,
        help="Delimiter used in the input CSV File",
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        filepath_X=args.filepath_x,
        filepath_Y=args.filepath_y,
        filepath_model=args.filepath_model,
        filepath_og_target=args.filepath_original_y,
        output=args.output,
        delimiter=args.delimiter,
    )
