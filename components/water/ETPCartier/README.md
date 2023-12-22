# ETP Cartier

## Overview

This script expects one file:

* CSV file with the necessary data to carry out the evapotranspiration calculation

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
python -m pytest
```


## Docker

### Build

Build the image with:

```sh
docker build -t enbic2lab/water/etp_cartier:1.0.0 .
```

### Run

Run the image with (assuming that the input files are in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/water/etp_cartier:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/etp_cartier:1.0.0 --filepath /mnt/shared/ETP_preprocessing.csv --delimiter ";" --output /mnt/shared/
```