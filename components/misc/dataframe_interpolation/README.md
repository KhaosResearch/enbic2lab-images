# Dataframe interpolation

## Overview
This script expects a CSV with NAs inside and will replace them using pandas interpolation. If wanted, columns may be excluded from interpolation using `--exclude-columns`. The interpolation method is decided by the user between these options, using `--interpolation-method`:

* ***none*** : If no interpolation is wanted.
* ***linear*** : Ignore the index and treat the values as equally spaced. This is the only method supported on MultiIndexes.
* ***time*** : Works on daily and higher resolution data to interpolate given length of interval. Only usable on Series or DataFrames with a DatetimeIndex.
* ***index*** : Use the actual numerical values of the index.
* ***values*** : Use the actual numerical values of the index.
* ***ffill*** : Fill in NaNs using existing values
* ***nearest*** : Passed to `scipy.interpolate.interp1d`
* ***zero*** : Passed to `scipy.interpolate.interp1d`
* ***slinear*** : Passed to `scipy.interpolate.interp1d`
* ***quadratic*** : Passed to `scipy.interpolate.interp1d`
* ***cubic*** : Passed to `scipy.interpolate.interp1d`
* ***spline*** : Passed to `scipy.interpolate.UnivariateSpline`.
* ***barycentric*** : Passed to `scipy.interpolate.interp1d`
* ***polynomial*** : Passed to `scipy.interpolate.interp1d`
* ***krogh*** : Wrappers around the SciPy interpolation methods of similar names.
* ***piecewise_polynomial*** : Wrappers around the SciPy interpolation methods of similar names.
* ***cubicspline*** : Wrappers around the SciPy interpolation methods of similar names.
* ***pchip*** : Wrappers around the SciPy interpolation methods of similar names.
* ***akima*** : Wrappers around the SciPy interpolation methods of similar names.
* ***from_derivatives*** : Refers to `scipy.interpolate.BPoly.from_derivatives`.

> For further information visit [pandas documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html).
        

## Usage
Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then run the script with:
```sh
python main.py --help
```

## Test
Install the requirements for testing:
```sh
python -m pip install -r requirements-dev.txt
```
Run the tests with:

```sh
python -m pytest
```
#Docker

### Build
Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/misc/dataframe_interpolation:1.0.1 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directoryit can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/dataframe_interpolation:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/dataframe_interpolation:1.0.1 --filepath "/mnt/shared/input.csv" --delimiter ";" --interpolation-method linear
```
> Output file path may be changed using `--output-path` argument.
> **Note**: If wanted, columns may be excluded using `--exclude-columns` and inserting the (case sensitive) names of the columns to not use for interpolation. By default none is excluded.
