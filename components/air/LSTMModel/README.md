# LSTM model

## Overview

Given some parameters, builds a ConvLSTM model for timeseries analysis.
Returns the built Keras model and X_test, y_test to make predictions

### Input
- filepath_X (str) --> File path of the x_test.
- filepath_y (str) --> File path of the y_test
- n_neurons (int) --> number of neurons to set the model (ej: 100, 200, 500)
- delimiter (str) --> Delimiter of the CSV File.
- n_steps_in (int) --> Time window to train the model
- n_steps_out (int) --> Period of time to predict

### Outputs
- lstm_X_test.npy
- lstm_Y_test.npy
- lstm_model.h5

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
docker build -t enbic2lab/air/lstm_model:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_model:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/lstm_model:1.0.0  --filepath-X "/mnt/shared/sequences_X.npy" --filepath-Y "/mnt/shared/sequences_Y.csv" --output "/mnt/shared/" --n-neurons 200 --n-steps-in 12 --n-steps-out 12 --delimiter ";"
```