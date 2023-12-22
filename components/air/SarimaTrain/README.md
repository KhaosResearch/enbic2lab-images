# Sarima train

## Overview

Train SARIMA model with a specific scaled dataset and evaluate it. This component returns the predictions made by the evaluation and the metrics obtained.

### Input
split_dataset.csv

### Outputs
- Sarima_predictions.csv
- Sarima_metrics.csv

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
docker build -t enbic2lab/air/sarima_train:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/sarima_train:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/sarima_train:1.0.0  --delimiter ";" --seasonality 12 --filepath "mnt/shared/split_dataset.csv" --output "/mnt/shared/" --date-column "fecha" --pollen-column "Platanus" --validation-time "2020-01-01"
```