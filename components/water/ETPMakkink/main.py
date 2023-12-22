import pandas as pd
from argparse import ArgumentParser
import numpy as np

def main(
        filepath: str,
        delimiter: str,
        output: str,
):
    df = pd.read_table(filepath, delimiter=delimiter)

    df["Pendiente sat vapor agua 1 (Makkink)"] = 4098 * 0.6108 * np.exp(17.27 * df['TMedia'] /(df['TMedia'] + 237.3))
    df["Pendiente sat vapor agua 2 (Makkink)"] = (df['TMedia'] + 237.3) ** 2
    df["P (Makkink)"] = 101.3 * (((293 - 0.0065 * 720) / 293) ** 5.26)
    df["Y (Makkink)"] = 0.665 * 10 ** -3 * df["P (Makkink)"] * 7.5
    df["ETP Makkink"] = 0.61 * df["Rs"] * (df["Pendiente sat vapor agua 2 (Makkink)"] / (df["Pendiente sat vapor agua 2 (Makkink)"] + df["Y (Makkink)"])) - 0.12

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Makkink")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file with the necessary data to carry out the evapotranspiration calculation.",
        required=True,
    )
    
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of input file",
        default=";",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
        default="/mnt/shared/"
    )

    args = parser.parse_args()

    main(
        args.filepath,
        args.delimiter,
        args.output + "output.csv",
    )

    