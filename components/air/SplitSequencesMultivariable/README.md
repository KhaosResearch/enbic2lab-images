# Split Sequence Multivariable

## Overview
The LSTM model will learn a function that maps a sequence of past observations as input to an output observation. As such, the sequence of observations must be transformed into multiple examples from which the LSTM can learn.

This script expects two sequences in CSV format:

- (`features.csv`): Multiple Input Series from Meteorological Variables
- (`target.csv`): pollen time series

### OUTPUTS
Generates supervised data from a multidimensional array.
Returns both data and its target for supervised learning.
This is the exact three-dimensional structure expected by an LSTM as input:

`(n_samples, time_window, n_features)`.


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
docker build -t enbic2lab/air/split_sequences_multivariable:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/split_sequences_multivariable:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/split_sequences_multivariable:1.0.0 --filepath-features "/mnt/shared/features.csv" --filepath-target "/mnt/shared/target.csv" --delimiter ";" --n-steps-in 12 --n-steps-out 12 --output "/mnt/shared/"
```