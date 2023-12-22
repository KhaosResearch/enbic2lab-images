import pandas as pd
from argparse import ArgumentParser
import numpy as np

def main(
        filepath: str,
        delimiter: str,
        k: float,
        output: str,
):
    df = pd.read_table(filepath, delimiter=delimiter)

    df["K(CTE)(Hamon)"] = k
    df["(-) tangente de la declinacion en radianes (Hamon)"] = -np.tan(df["Declinación RAD"])
    df["Tangente de la latitud en radianes (Hamon)"] = np.tan(df["Latitud RAD"])
    df["Coseno (Hamon)"] = np.cos((df["(-) tangente de la declinacion en radianes (Hamon)"])*(df["Tangente de la latitud en radianes (Hamon)"]))**(-1)
    df["N (Hamon)"] = (24/3.141592)*(df["Coseno (Hamon)"])
    df["ETP Hamon"] = df["K(CTE)(Hamon)"]*0.165*216.7*df["N (Hamon)"]*((0.6108*np.exp(((17.27*df["TMedia"])/(237.3 + df["TMedia"]))))/(df["TMedia"] + 273.3))

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Hamon")
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
        "--k",
        type=float,
        help="K value",
        required=True,
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
        args.k,
        args.output + "output.csv",
    )

    