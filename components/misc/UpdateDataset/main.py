import pandas as pd
import argparse


def main(
    first_file: str,
    second_file: str,
    name_column_date_first_file: str,
    name_column_date_second_file: str,
    output: str,
    col_first_file: str,
    col_second_file: str,
    delimiter_first_file: str = ";",
    delimiter_second_file: str = ";",
):
    main_dataframe = pd.read_csv(first_file, sep=delimiter_first_file)
    main_dataframe = main_dataframe.drop(col_first_file, axis=1)
    aux_dataframe = pd.read_csv(second_file, sep=delimiter_second_file)
    aux_dataframe = aux_dataframe.rename(columns={col_second_file: col_first_file})
    main_dataframe = main_dataframe.join(
        aux_dataframe.set_index(name_column_date_second_file), on=name_column_date_first_file
    )

    main_dataframe.to_csv(output, sep=delimiter_first_file, index=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP Plot component")

    # Define command-line arguments
    parser.add_argument(
        "--first-file", type=str, required=True, help="Path to the input first CSV file", default="/mnt/shared/6155A_aemet_pollen_meteo_platanus_data_split.csv"
    )
    parser.add_argument(
        "--second-file",
        type=str,
        default="/mnt/shared/6155A_completed.csv",
        required=True,
        help="Path to the input second CSV file",
    )
    parser.add_argument(
        "--name-column-date-first-file",
        type=str,
        default="fecha",
        required=True,
        help=" Column of the main file used to join with the aux file as key",
    )
    parser.add_argument(
        "--name-column-date-second-file",
        type=str,
        default="DATE",
        required=True,
        help="Column of the aux file used to join with te main file as key.",
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output CSV file "
    )
    parser.add_argument(
        "--col-first-file",
        type=str,
        default="prec",
        required=True,
        help="Column of the main file to be updated.",
    )
    parser.add_argument(
        "--col-second-file",
        type=str,
        default="6155A",
        required=True,
        help="Column of the aux file used to update de main file",
    )
    parser.add_argument(
        "--delimiter-first-file",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the first input CSV File",
    )
    parser.add_argument(
        "--delimiter-second-file",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the second input CSV File",
    )
    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.first_file,
        args.second_file,
        args.name_column_date_first_file,
        args.name_column_date_second_file,
        args.output,
        args.col_first_file,
        args.col_second_file,
        args.delimiter_first_file,
        args.delimiter_second_file,
    )