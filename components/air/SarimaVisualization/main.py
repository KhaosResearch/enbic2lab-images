from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from numpy import loadtxt

def main(filepath: str, filepath_prediction: str, output: str, validation_time: str, delimiter: str = ";", date_column:str="fecha"):
    """
    Given the prediction array, pollen type and the start date for validation

    Returns the R2 visualisation
    """

    dataset = pd.read_csv(filepath, sep=delimiter, index_col=date_column)
    mask = dataset.index >= validation_time
    dataset_pred = dataset.loc[mask]
    if dataset_pred.empty:
        print("No data available for the specified validation time.")
        return
    
    prediction = loadtxt(filepath_prediction, delimiter=delimiter)
    pred = pd.DataFrame()
    pred["pred"] = prediction
    pred[date_column] = dataset_pred.index
    pred = pred.set_index(date_column)

    ax = dataset[validation_time:].plot(label="observed", figsize=(14, 7))
    pred.plot(ax=ax, label="Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Pollen / m3")
    plt.legend(["Actual Data", "Pollen Prediction"])

    # Save plot in png
    suffix = ".png"
    outfile_sarima_plot = "Sarima_visualisation"
    path = Path(output, outfile_sarima_plot).with_suffix(suffix)
    plt.savefig(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima visualization")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/Sarima_Y_test.csv",
        required=True,
        help="File path of X_test csv file",
    )
    parser.add_argument(
        "--filepath-prediction",
        type=str,
        default="/mnt/shared/Sarima_predictions.csv",
        required=True,
        help="File path of Y_test csv file",
    )
    parser.add_argument(
        "--validation-time",
        type=str,
        default="2020-01-01",
        required=True,
        help="Indicate from which period of time you want to make the validation",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default="fecha",
        required=True,
        help="Indicate which is the name of column date.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        required=True,
        help="Path to the outputs files",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.filepath_prediction,
        args.output,
        args.validation_time,
        args.delimiter,
        args.date_column
    )
