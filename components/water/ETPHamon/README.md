# ETP Hamon

## Overview

This script expects one file:

* A CSV file with the necessary data to carry out the evapotranspiration calculation


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
docker build -t $REGISTRY/enbic2lab/water/etp_hamon:1.0.0 .
```

### Run

Run the image with (assuming that the input files are in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/water/etp_hamon:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/etp_hamon:1.0.0 --filepath /mnt/shared/ETP_preprocessing.csv --delimiter ";" --k 1.75 --output /mnt/shared/
```