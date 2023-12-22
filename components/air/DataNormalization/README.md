# Data Normalization for time series data

## Overview

This script expects a CSV file with the following columns:

- `Fecha`: Date Column.
- `Polen type`: Type of pollen to be studied.
- `Meteorological Variables`: Meteorological Variables such wind, temperature, etc.

e.g.:

```csv
Fecha;Platanus;feature1;feature2
2023-01-01;1;2;4
2023-02-01;3;6
2023-03-01;5;7
```
### OUTPUTS
Given a pandas dataframe, it's split in two dataframes (features and target) and then they are normalized with MinMaxScaler 
    
Returns two normalized dataframes (features and target) and their scalers

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
docker build -t enbic2lab/air/data_normalization:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/data_normalization:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/data_normalization:1.0.0 --filepath "/mnt/shared/split_dataset.csv" --delimiter ";" --date-column "fecha" --pollen-column "Platanus" --output "/mnt/shared/"
```