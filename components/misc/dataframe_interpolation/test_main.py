import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from pandas import NA
from filecmp import cmp

from main import dataframe_interpolation

input_CSV_data = pd.DataFrame(
    data={
        "A": [1, 2, 3, 4, 5, 6, None],
        "B": [6, 7, 8, 9, None, 11, 12],
        "C": [11, None, 13, 14, 15, 16, 17],
        "D": [16, 17, 18, None, 20, 21, 22],
    }
)



def test_dataframe_interpolation():
    delimiter = ";"
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
        ]
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)

        for choice in choices:
            print(f"Testing {choice}...", end="")
            if choice == "time":
                with pytest.raises(ValueError):
                    dataframe_interpolation(
                        filepath=temp_input_file,
                        delimiter=delimiter,
                        interpolation_method=choice,
                        exclude_columns=None,
                        output=temp_output_file,
                    )
                continue
            else:
                dataframe_interpolation(
                    filepath=temp_input_file,
                    delimiter=delimiter,
                    interpolation_method=choice,
                    exclude_columns=None,
                    output=temp_output_file,
                )

            assert os.path.exists(temp_output_file)
            print("OK", end=".")
            assert os.path.getsize(temp_output_file) > 0
            print("OK")



def test_dataframe_interpolation_error():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=delimiter)

        with pytest.raises(ValueError):
            dataframe_interpolation(
                filepath=temp_input_file,
                delimiter=delimiter,
                interpolation_method="wrong",
                exclude_columns=None,
                output=temp_output_file,
            )
        assert not os.path.exists(temp_output_file)
        
        with pytest.raises(ValueError):
            dataframe_interpolation(
                filepath=temp_input_file,
                delimiter=delimiter,
                interpolation_method="none",
                exclude_columns="wrong-column",
                output=temp_output_file,
            )
        assert not os.path.exists(temp_output_file)

