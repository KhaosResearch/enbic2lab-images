import argparse
import pandas as pd


def lagged_time_series(filepath: str, delimiter: str, date_column: str, lags: int, pollen_column: str, output: str):
    """
    Given a pollen dataframe and number of lags, it produces a lagged dataframe

    Returns a lagged dataframe
    """
    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter)
    dataframe = dataframe.set_index(date_column)

    # Remove target Column to make lags
    df = dataframe.drop([pollen_column], axis=1)
    df_atr = dataframe[df.columns]

    # Crear columnas lagged usando pd.concat
    lags_range = range(1, int(lags) + 1)
    lagged_columns = []
    for lag in lags_range:
        lagged_data = df_atr.shift(lag)
        lagged_data.columns = [f"{col} (t-{lag})" for col in lagged_data.columns]
        lagged_columns.append(lagged_data)

    # Concatenar todas las columnas lagged y la columna de polen
    lagged_df = pd.concat([dataframe] + lagged_columns, axis=1)

    # Eliminar filas con valores NaN
    lagged_df = lagged_df.dropna()

    # Guardar Outfile
    lagged_df.to_csv(output, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make lagged data in time series data")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Input CSV file path.",
    )
    parser.add_argument("--delimiter", type=str, default=";", help="Delimiter used in CSV.")
    parser.add_argument("--date-column", type=str, default="fecha", help="Name of the date column")
    parser.add_argument("--lags", type=int, default=12, help="Select number of lags")
    parser.add_argument("--pollen-column", type=str, help="Name of pollen column")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/lagged_time_series.csv",
        help="Output CSV file path.",
    )
    args = parser.parse_args()

    lagged_time_series(args.filepath, args.delimiter, args.date_column, args.lags, args.pollen_column,
                       args.output)
