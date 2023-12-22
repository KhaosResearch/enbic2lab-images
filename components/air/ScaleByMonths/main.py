import argparse
import pandas as pd


def scale_by_months(filepath: str, delimiter: str, date_column: str, output: str) -> None:
    """
        Given a Pollen Dataframe by days, it is scaled to months.
        Returns the scaled Dataframe in months.

        Args:
            filepath (str): The path to the CSV dataset file to be scaled.
            delimiter (str): Delimiter to use in the output CSV file to separate values (e.g., ',' or ';').
            date_column (str): Column date name in the CSV.
            output (str): The path to save the scaled dataset as a new CSV file.

        Example:
            To split a dataset 'data.csv' by selecting attributes 'A', 'B', and 'C', and save the resulting dataset as 'output.csv' with a semicolon (';') as the delimiter:

            >>> scale_by_months(filepath="data.csv", delimiter=';', date_column='fecha', output="scaled_dataset.csv")

        Note:
            - The resulting dataset is saved with the specified delimiter.
        """

    try:
        dataframe = pd.read_csv(filepath, sep=delimiter, parse_dates=[date_column])
    except FileNotFoundError:
        print(f"File {filepath} not found.")
    except KeyError:
        raise print(f"the column '{date_column}' does not exist in the dataframe.")

    # Formatear las fechas para incluir solo año y mes
    dataframe[date_column] = dataframe[date_column].dt.to_period('M')

    # Agrupar datos por mes y sumar los valores
    try:
        df_month = dataframe.groupby(date_column).sum()
    except Exception as e:
        raise Exception(f"Error al agrupar los datos por mes: {e}")

    # Guardar el archivo de salida
    try:
        df_month.to_csv(output, sep=delimiter)
    except Exception as e:
        raise Exception(f"Error al guardar el archivo de salida: {e}")


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the altitude range of each community.")
    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the csv file",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        help="Delimiter of the input file and output file",
        required=True,
        metavar="CHAR"
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default="fecha",
        help="Date column in pollen dataset",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared/",
        metavar="STRING",
        dest="output",
    )


    args = parser.parse_args()

    scale_by_months(
        filepath=args.filepath,
        delimiter=args.delimiter,
        date_column=args.date_column,
        output= args.output + "scaled_dataset.csv"
    )
