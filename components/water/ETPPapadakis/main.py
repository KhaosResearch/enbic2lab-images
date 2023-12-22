
import pandas as pd
import numpy as np
from argparse import ArgumentParser

def main(
    filepath: str,
    delimiter: str,
    output: str
):

  
    df = pd.read_csv(filepath, sep=delimiter)
    
    df["PVMAX"] = np.exp(
        60.433
        - 6834.271 / (df["TMAX"] + 273.16)
        - 5.16923 * np.log(df["TMAX"] + 237.16)
    ) / 100

    df["PVMIN"] = np.exp(
        60.433
        - 6834.271 / (df["TMIN"] + 273.16)
        - 5.16923 * np.log(df["TMIN"] + 237.16)
    ) / 100

    df["ETP Papadakis"] = (0.5625 * (df["PVMAX"] - df["PVMIN"]) * 10) / 28


    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Papadakis")
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

    