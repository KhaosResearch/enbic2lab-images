# Split by Datetime pollen time series data

## Overview

This script expects a CSV file with the following columns:

- `Fecha`: Date Column.
- `Polen type`: Type of pollen to be studied.
- `Meteorological Variables`: Meteorological Variables such wind, temperature, etc.

e.g.:

```csv
Fecha;Platanus;Meteorological Variables
2023-01-01;1;2
2023-02-01;3;
2023-03-01;5;
```
### OUTPUTS
Returns a portion of the original dataset (`split_dataset.csv`)


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
docker build -t enbic2lab/air/split_by_datetime:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/split_by_datetime:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/split_by_datetime:1.0.0 --filepath "/mnt/shared/scaled_dataset.csv" --delimiter ";" --date-column "fecha" --start-date "1992-01-01" --end-date "2021-01-01"
```