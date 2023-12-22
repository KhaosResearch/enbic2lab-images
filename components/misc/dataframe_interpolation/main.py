from re import findall
import pandas as pd
from typing import List

from argparse import ArgumentParser


# ========= METHODS =========
def dataframe_interpolation(
    filepath: str,
    output: str,
    delimiter: str = ";",
    interpolation_method: str = "none",
    exclude_columns: List[str] = None,
) -> None:
    """Perform data interpolation on a CSV dataset and save the interpolated dataset to a new CSV file.

    This function reads a CSV dataset, performs data interpolation using the specified interpolation method, and saves the interpolated dataset to a new CSV file. You can also exclude specific columns from interpolation.

    Args:
        filepath (str): The path to the CSV dataset file to be interpolated.
        delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the interpolated dataset as a new CSV file.
        interpolation_method (str): The method for data interpolation. Options include: "none" (no interpolation), "linear," "time," "index," and various other methods supported by Pandas' interpolate function. Default is "none."
        exclude_columns (List[str]): A list of column names to exclude from interpolation. Default is None.

    Raises:
        ValueError: If an invalid interpolation method is specified or if any of the exclude columns are not found in the dataset.

    Example:
        To interpolate a dataset 'data.csv' using linear interpolation, exclude columns 'A' and 'B' from interpolation, and save the interpolated dataset as 'interpolated_data.csv' with a semicolon (';') as the delimiter:
        
        >>> dataframe_interpolation(filepath="data.csv", delimiter=";", output="interpolated_data.csv", interpolation_method="linear", exclude_columns=["A", "B"])

    Note:
        - You can exclude specific columns from interpolation by providing their names in the exclude_columns list (case sensitive).
        - The interpolated dataset is saved with the specified delimiter.
    """

    data = pd.read_csv(filepath, sep=delimiter)

    if exclude_columns is not None:
        try:
            y_columns = data[exclude_columns]
            data = data.drop(exclude_columns, axis=1)
        except KeyError:
            raise ValueError(
                f"Column(s) {exclude_columns} not found in the CSV file. Possible columns: {list(data)}"
            )

    match interpolation_method.lower():
        case "none":
            data = data
        case "linear" | "time" | "index" | "values" | "ffill" | "nearest" | "zero" | "slinear" | "quadratic" | "cubic" | "barycentric" | "krogh" | "piecewise_polynomial" | "cubicspline" | "pchip" | "akima" | "from_derivatives":
            data = data.infer_objects(copy=False)
            data = round(
                data.interpolate(method=interpolation_method, inplace=False), 3
            )
        case "polynomial" | "spline":
            data = data.infer_objects(copy=False)
            data = round(
                data.interpolate(method=interpolation_method, inplace=False, order=3), 3
            )
        case _:
            raise ValueError(
                f"Interpolation method {interpolation_method} not supported"
            )

    if exclude_columns is not None:
        data = pd.concat([y_columns, data], axis=1)

    data.to_csv(output, sep=delimiter, index=None)


# ========= MAIN =========
if __name__ == "__main__":
    parser = ArgumentParser(description="Interpolate NAs from a CSV File")
    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the CSV File",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV File",
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--interpolation-method",
        dest="interpolation_method",
        type=str,
        help="Interpolation technique to use (Not case sensitive). For more info see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html",
        required=False,
        choices=[
            "none",  # Don’t interpolate. CSV NaNs will not be filled.
            "linear",  # Ignore the index and treat the values as equally spaced. This is the only method supported on MultiIndexes.
            "time",  # Works on daily and higher resolution data to interpolate given length of interval.
            "index",  # use the actual numerical values of the index.
            "values",  # use the actual numerical values of the index.
            "ffill",  # Fill in NaNs using existing values
            "nearest",  # Passed to scipy.interpolate.interp1d
            "zero",  # Passed to scipy.interpolate.interp1d
            "slinear",  # Passed to scipy.interpolate.interp1d
            "quadratic",  # Passed to scipy.interpolate.interp1d
            "cubic",  # Passed to scipy.interpolate.interp1d
            "spline",  # Passed to scipy.interpolate.UnivariateSpline.
            "barycentric",  # Passed to scipy.interpolate.interp1d
            "polynomial",  # Passed to scipy.interpolate.interp1d
            "krogh",  # Wrappers around the SciPy interpolation methods of similar names.
            "piecewise_polynomial",  # Wrappers around the SciPy interpolation methods of similar names.
            "cubicspline",  # Wrappers around the SciPy interpolation methods of similar names.
            "pchip",  # Wrappers around the SciPy interpolation methods of similar names.
            "akima",  # Wrappers around the SciPy interpolation methods of similar names.
            "from_derivatives"  # Refers to scipy.interpolate.BPoly.from_derivatives.
            # For more info visit https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html
        ],
        default="none",
    )
    parser.add_argument(
        "--exclude-columns",
        dest="exclude_columns",
        type=str,
        help="Columns to exclude from interpolation. Include non numeric value columns separated by commas (,)",
        required=False,
        metavar="STRING",
        default=None,
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Output file path",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    args.exclude_columns = args.exclude_columns.replace(" ", "").split(",") if args.exclude_columns else None

    dataframe_interpolation(
        filepath=args.filepath,
        delimiter=args.delimiter,
        interpolation_method=args.interpolation_method,
        exclude_columns=args.exclude_columns,
        output=args.output+"/output.csv",
    )
