# Random forest regression

## Overview

Randon forest regression from CSV file

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
docker build -t enbic2lab/misc/random_forest_regression:1.0.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/misc/random_forest_regression:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/misc/random_forest_regression:1.0.0 --filepath "mnt/shared/6155A_aemet_pollen_meteo_olea_data_updated_mean_statistics.csv" --delimiter ";" --date-column "Date" --dependent-variable "Olea"
```