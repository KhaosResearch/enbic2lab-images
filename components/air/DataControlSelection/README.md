# Choose Metrics CSV

## Overview

Select the best CSV by metrics comparation.

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
docker build -t enbic2lab/misc/choose_metrics_csv:1.0.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/misc/choose_metrics_csv:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/misc/choose_metrics_csv:1.0.0 --filepath-metrics "/mnt/shared/6155A_aemet_pollen_meteo_platanus_metrics.csv" --filepath-pandas "/mnt/shared/6155A_aemet_pollen_meteo_platanus_data_updated_linear_interpolation_statistics.csv" --filepath-mean "/mnt/shared/6155A_aemet_pollen_meteo_platanus_data_updated_mean_interpolation_statistics.csv"  --delimiter ";" --output "/mnt/shared/output.csv"
```