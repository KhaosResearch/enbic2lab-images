# LSTM evaluation

## Overview

Given X_test, y_test and the trained model, make predictions and evaluate the model

Returns the model' metrics

### PARAMETERS
- filepath_X (str) --> File path of the x_test.
- filepath_y (str) --> File path of the y_test 
- filepath_model (str) --> File path of the model
- filepath_original_y (str) --> File path of the target dataset used for data normalization
- delimiter (str) --> Delimiter of the CSV File.

### OUTPUTS
- lstm_metrics.csv
- lstm_predictions.csv

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
docker build -t enbic2lab/air/lstm_evaluation:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_evaluation:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_evaluation:1.0.1  --filepath-x "mnt/shared/lstm_X_test.npy" --filepath-y "mnt/shared/lstm_Y_test.npy" --filepath-model "mnt/shared/lstm_model.h5" --filepath-original-y "mnt/shared/target.csv" --delimiter ";" --output "/mnt/shared/"