import pandas as pd
import argparse


def main(
    filepath: str,
    output: str,
    delimiter: str = ",",
    ru: str = "50",
    etpname: str = "Hargreaves",
):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        ru (str): Parameter necessary to calculate the useful rainfall.
        etpname (str): Name of the ETP with which the useful rainfall is to be calculated.
        output (str): Path to save the output CSV file with computed LLU.
    """

    df = pd.read_table(filepath, delimiter=delimiter)

    etp_fullname = " ".join(["ETP", etpname])

    llu_first_day = df.loc[0, "Precipitación"] - float(ru)

    if llu_first_day < 0:
        df.loc[0, "LLU"] = 0
    else:
        df.loc[0, "LLU"] = llu_first_day

    for i in range(1, len(df)):
        sum_prep = df.loc[0 : i - 1, "Precipitación"].sum()
        sum_etp = df.loc[0:i, etp_fullname].sum()
        sum_llu = df.loc[0 : i - 1, "LLU"].sum()
        llu = sum_prep - float(ru) - sum_etp - sum_llu
        if llu < 0:
            df.loc[i, "LLU"] = 0
        else:
            df.loc[i, "LLU"] = llu

    df.to_csv(output, index=False, decimal=".", sep=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLU component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath", type=str, required=True, help="Path to the input CSV File"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--ru",
        type=str,
        default="50",
        required=True,
        help="Parameter necessary to calculate the useful rainfall",
    )
    parser.add_argument(
        "--etpname",
        type=str,
        default="Hargreaves",
        required=False,
        help="Name of the ETP with which the useful rainfall is to be calculated",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
        required=True,
        default="/mnt/shared/ComponentLLU.csv"
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.output,
        args.delimiter,
        args.ru,
        args.etpname,
    )
