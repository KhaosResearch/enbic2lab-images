
import pandas as pd
from argparse import ArgumentParser

def main(
    filepath: str,
    delimiter: str,
    output: str
):
    df = pd.read_csv(filepath, sep=delimiter)
    
    df["ETP Taylor"] = 0.6*df["Rs"]*(((df["TMedia"]+237.3)**2)/(((df["TMedia"]+237.3)**2) + (0.665*10**(-3)*(101.3*(((293-0.0065*720)/293)**5.26))*7.5)))  

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Taylor")
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

    