import pandas as pd
from argparse import ArgumentParser
import numpy as np

def main(
        filepath: str,
        delimiter: str,
        output: str,
):
    df = pd.read_table(filepath, delimiter=delimiter)

    df["E1 (minimas) (Jensen-Haise)"] = 6.108 * np.exp((17.27 * df["TMIN"]) / (df["TMIN"] + 237.3))
    df["E2 (maximas) (Jensen-Haise)"] = 6.108 * np.exp((17.27 * df["TMAX"])/(df["TMAX"] + 237.3))
    df["CT (Jensen-Haise)"] = 1 / (38 - (720 / 152.5) + (380 / (df["E2 (maximas) (Jensen-Haise)"] - df["E1 (minimas) (Jensen-Haise)"])))
    df["Tx (Jensen-Haise)"] = -2.5 - 0.14 * (df["E2 (maximas) (Jensen-Haise)"] - df["E1 (minimas) (Jensen-Haise)"]) - (720 / 550)
    df["ETP Jensen-Haise"] = df["CT (Jensen-Haise)"] * (df["TMedia"] - df["Tx (Jensen-Haise)"]) * df["Ro EXTRATERRESTRE mm/dia"]
    

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Jensen-Haise")
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

    