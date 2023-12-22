from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from numpy import loadtxt

def main(filepath: str,filepath_predictions: str,output:str, start_date:str="2015-01-01", n_steps_out:int=12, delimiter: str = ";",pollen_column:str="Platanus", date_column:str="fecha"):
    """
    Given the complete dataset, the prediction array, pollen type and the start date

    Returns the R2 visualisation
    """

    # Load predictions array from CSV
    prediction = loadtxt(filepath_predictions, delimiter=delimiter)
    pred = pd.DataFrame()
    pred["pred"] = prediction

    # Load the complete dataset from CSV
    dataset = pd.read_csv(filepath, sep=delimiter, index_col=date_column)
    dataset.index = pd.to_datetime(dataset.index)
    dates = dataset.index[-n_steps_out:]

    pred[date_column] = dates
    pred = pred.set_index(date_column)

    ax = dataset[start_date:][pollen_column].plot(label="observed", figsize=(14, 7))
    pred.plot(ax=ax, label="Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Pollen / m3")
    plt.legend(["Actual Data", "Pollen Prediction"])

    # Save plot in png
    suffix = ".png"
    path = Path(output, "lstm_visualisation").with_suffix(suffix)
    plt.savefig(path)
    # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima model")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/split_dataset.csv",
        required=True,
    )
    parser.add_argument(
        "--filepath-predictions",
        type=str,
        default="/mnt/shared/lstm_predictions.csv",
        required=True,
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2015-01-01",
        required=True,
    )
    parser.add_argument(
        "--n-steps-out",
        type=int,
        default=12,
        required=True,
    )
    parser.add_argument(
        "--pollen-column", 
        type=str, 
        help="Name of pollen column")
    parser.add_argument(
        "--date-column", 
        type=str, 
        default="fecha", 
        help="Name of the date column")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        required=True,
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.filepath_predictions,
        args.output,
        args.start_date,
        args.n_steps_out,
        args.delimiter,
        args.pollen_column, 
        args.date_column,
    )
