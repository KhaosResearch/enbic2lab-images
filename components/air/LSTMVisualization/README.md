# LSTM visualization model

## Overview

Given the complete dataset, the prediction array, pollen type and the start date

Returns the R2 visualisation of the predictions

### Input

- split_dataset.csv
- lstm_predictions.csv

### Outputs
- lstm_visualisation.png

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
docker build -t enbic2lab/air/lstm_visualization:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_visualization:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_visualization:1.0.0 --filepath "mnt/shared/split_dataset.csv" --filepath-predictions "mnt/shared/lstm_predictions.csv" --delimiter ";" --start-date "2015-01-01" --n-steps-out 12 --output "/mnt/shared/" --pollen-column "Platanus" --date-column "fecha"