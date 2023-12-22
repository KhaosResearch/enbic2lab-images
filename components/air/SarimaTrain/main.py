import math
from itertools import product
from pathlib import Path
import argparse
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import statsmodels.api as sm
from numpy import ndarray, savetxt


def parameter_configuration():
    ps = [0, 1, 2]
    d = [0, 1]
    qs = [0, 1, 2, 3]
    Ps = [0, 1, 2]
    D = [0, 1]
    Qs = [0, 1, 2, 3]

    parameters = product(ps, d, qs, Ps, D, Qs)
    parameters_list = list(parameters)
    len(parameters_list)
    return parameters_list


def optimizeSARIMA(df, parameters_list, s,pollen_column):
    """Return dataframe with parameters and corresponding AIC

    parameters_list - list with (p, q, P, Q) tuples
    d - integration order in ARIMA model
    D - seasonal integration order
    s - length of season
    """

    results = []
    best_aic = float("inf")

    for param in parameters_list:
        # we need try-except because on some combinations model fails to converge
        try:
            model = sm.tsa.statespace.SARIMAX(
                endog=df[pollen_column],
                exog=df.drop([pollen_column], axis=1),
                order=(param[0], param[1], param[2]),
                seasonal_order=(param[3], param[4], param[5], s),
                enforce_stationarity=False,
                enforce_invertibility=False,
            ).fit(disp=False)
        except:
            continue
        aic = model.aic
        # saving best model, AIC and parameters
        if aic < best_aic:
            best_model = model
            best_aic = aic
            best_param = param
        results.append([best_param, best_model.aic])

    if not results:
        return pd.DataFrame(columns=["parameters", "aic"])

    result_table = pd.DataFrame(results)
    result_table.columns = ["parameters", "aic"]
    # sorting in ascending order, the lower AIC is - the better
    result_table = result_table.sort_values(by="aic", ascending=True).reset_index(
        drop=True
    )

    return result_table


def compute_metrics(test: ndarray, pred: ndarray) -> dict:
    """
    Provided the forecasted and test data, computes several metrics.

    Returns a dictionary of metrics
    """
    mae_lstm = mean_absolute_error(test, pred)
    rmse_lstm = math.sqrt(mean_squared_error(test, pred))
    r2_lstm = r2_score(test, pred)

    return {"MAE": mae_lstm, "RMSE": rmse_lstm, "R2 Score": r2_lstm}


def trainSARIMA(
    X: pd.DataFrame, Y: pd.DataFrame, seasonality: int, params: dict
) -> sm.tsa.statespace.SARIMAX:
    """Train SARIMA model with the best parameters
    Provided the dataframe, parameters and seasonality of the data, train SARIMA model and return it.

    Return a trained SARIMA model
    """
    model = sm.tsa.statespace.SARIMAX(
        endog=Y,
        exog=X,
        order=(params["p"], params["d"], params["q"]),
        seasonal_order=(params["P"], params["D"], params["Q"], seasonality),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)

    return model


def evaluateSARIMA(
    model: sm.tsa.statespace.SARIMAX,
    X_test: pd.DataFrame,
    y_test: pd.DataFrame,
    validation_time: str,
    pollen_column:str
) -> (pd.DataFrame, dict):
    prediction = model.get_prediction(
        start=pd.to_datetime(validation_time), dynamic=False
    )

    prediction = prediction.predicted_mean

    # forecast = load_model.get_forecast(steps=90)

    mask = y_test.index >= validation_time
    y_pred = y_test.loc[mask]
    # y_pred = y.iloc[-15:]

    # metrics = compute_metrics(dataframe_pred[pollen_column].values, prediction)
    metrics = compute_metrics(y_pred[pollen_column], prediction)

    return prediction, metrics


def main(
    filepath: str,
    output: str,
    delimiter: str = ";",
    seasonality: str = 12,
    date_column: str = "fecha",
    validation_time: str = "2020-01-01",
    pollen_column:str="Platanus"
):
    """
    Train SARIMA model with a specific scaled dataset and evaluate it using the validation_time.
    Return a the predictions made by the tests and the metrics obtained.
    """

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter)
    dataframe[date_column] = pd.to_datetime(dataframe[date_column])
    dataframe = dataframe.set_index(date_column)
    dataframe.index.freq = "MS"  # Agregar esta línea

    # Split dataframe in features/target
    Y = dataframe[[pollen_column]]
    X = dataframe.drop([pollen_column], axis=1)
    # Set configuration parameters for SARIMA hyperparameter optimization
    # parameters_list = parameter_configuration()
    # result_table = optimizeSARIMA(dataframe, parameters_list, seasonality, pollen_column)

    # set the best parameters that give the lowest AIC
    # p, d, q, P, D, Q = result_table.parameters[0]
    params = {
        "p": 1,
        "d": 0,
        "q": 0,
        "P": 0,
        "D": 1,
        "Q": 0,
    }

    # Train SARIMA model
    model = trainSARIMA(X, Y, seasonality, params)

    # Save X dataframe as CSV
    suffix = ".csv"

    outfile_X = "features"
    path_X = Path(output, outfile_X).with_suffix(suffix)
    X.to_csv(path_X, sep=delimiter)

    # Save Y dataframe as CSV
    outfile_Y = "target"
    path_Y = Path(output, outfile_Y).with_suffix(suffix)
    Y.to_csv(path_Y, sep=delimiter)

    # Evaluate SARIMA model
    X_test = X
    y_test = Y

    prediction, metrics = evaluateSARIMA(model, X_test, y_test, validation_time, pollen_column)

    # Save metrics and predictions
    outfile_metrics = "Sarima_metrics"
    # Save metrics in dataframe CSV
    df_metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
    path = Path(output, outfile_metrics).with_suffix(suffix)
    df_metrics.to_csv(path, sep=delimiter)

    # Save predictions numpy array as CSV
    outfile_name_prediction = "Sarima_predictions"
    path_predictions = Path(output, outfile_name_prediction).with_suffix(suffix)
    savetxt(path_predictions, prediction, delimiter=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima model")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/split_dataset.csv",
        required=True,
        help="Path to the input CSV file with the data needed to build the corresponding graph",
    )
    parser.add_argument(
        "--seasonality",
        type=int,
        default=12,
        required=False,
        help="Set the seasonality of your pollen",
    )
    parser.add_argument(
        "--pollen-column",
        type=str,
        default="Platanus",
        required=False,
        help="Name of the pokllen column",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default="fecha",
        required=False,
        help="Name of the date column",
    )
    parser.add_argument(
        "--validation-time",
        type=str,
        default="2020-01-01",
        required=False,
        help="Indicate from which period of time you want to make the validation",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=False,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        required=False,
        help="Path to the output where files are saved",
    )

    args = parser.parse_args()
    print(args)
    # Call the main function with provided arguments and specify the output file path
    main(
        filepath=args.filepath,
        output=args.output,
        delimiter=args.delimiter,
        seasonality=args.seasonality,
        date_column=args.date_column,
        validation_time=args.validation_time,
        pollen_column=args.pollen_column
    )
