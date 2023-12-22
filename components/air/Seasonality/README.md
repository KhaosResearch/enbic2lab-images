# Study stationary and seasonality of pollen time series data
Generate different plots based on ARIMA methods.

## Overview

This script expects a CSV file with the following columns:

- `Fecha`: Date Column.
- `Polen type`: Type of pollen to be studied.

e.g.:

```csv
Fecha;Platanus;
2023-01-01;1;
2023-01-02;3;
2023-01-03;5;
```
### OUTPUTS
* SARIMAX_plots.pdf
* DickerFuller_seasonality.csv
* seasonality.pdf
* DickeyFuller_plot.pdf

## Usage

Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then, run the script with:

```sh
python main.py --help
```

## Tests

Install the requirements for testing:

```sh
python -m pip install -r requirements-dev.txt
```

Run the tests with:

```sh
python test_main.py
```

## Docker

### Build

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/air/seasonality:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/seasonality:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/seasonality:1.0.1 --filepath "/mnt/shared/filepath.csv" --delimiter ";" --date-column "fecha" --pollen-column "Platanus" --year 2021
```