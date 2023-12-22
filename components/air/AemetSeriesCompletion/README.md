# Series Completion

## Overview
This component processes time series data from a CSV file, performing series completion for a specified target station using linear regression with given stations. It ranks analysis stations based on criteria like R-squared and slope, selects the best ones, and uses their data to fill missing values in the target station. The code offers options for testing the homogeneity of the completed series using methods like Pettitt, SNHT, and Buishand tests. Results are saved in separate CSV files.

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
## Docker

### Build
Build the image with:

```sh
docker build -t enbic2lab/water/series_completion_pollen:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/series_completion_pollen:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/series_completion_pollen:1.0.0 --filepath mnt/shared/input.csv --start-date 1991-05-11 --end-date 2021-09-30 --target-station "6155A" --analysis-stations "6172O,6156X" --completion-criteria r2 --tests "pettit" --delimiter ";"
```
> **Note**: Some parameters are optional:
>   - `--delimiter` is optional, if it is not declared, ";" will be used as default.
>   - `--tests` is optional, its default value is ["pettit", "snht", "buishand"].
>   - `--completion-criteria` is optional, its default value is ["r2", "slope", "pair"].

> **Note 2**: `--analysis-stations` may take more than one stations if they are in the given CSV file.