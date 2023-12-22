# Sarima visualization

## Overview

Given the prediction array, pollen type and the start date for validation

Returns the R2 visualisation

### Input
- Sarima_predictions.csv
- Sarima_Y_test.csv

### Outputs
- Sarima_visualisation.png

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
docker build -t enbic2lab/air/sarima_visualization:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/sarima_visualization:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/sarima_visualization:1.0.0  --filepath "mnt/shared/Sarima_Y_test.csv" --filepath-prediction "mnt/shared/Sarima_predictions.csv" --delimiter ";" --validation-time "2020-01-01" --output "/mnt/shared/"
```