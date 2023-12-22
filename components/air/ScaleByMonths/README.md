# Scale pollen dataset by months

## Overview

This script expects a CSV file with the following columns:

- `Fecha`: Columna fecha.
- `Polen type`: Type of pollen to be studied.
- `Meteorological variables`: Meteorological variables that will help to make predictions.

e.g.:

```csv
Fecha;Platanus;Meteorological variables
2023-01-01;1;2
2023-01-02;3;4
2023-01-03;5;6
```
Given a Pollen Dataframe by days, it is scaled to months returns a plot (`scaled_dataset.csv`).
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
docker build -t $REGISTRY/enbic2lab/air/scale_by_months:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/scale_by_months:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/scale_by_months:1.0.1 --filepath "/mnt/shared/filepath.csv" --delimiter ";" --date-column "fecha"
```