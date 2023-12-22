# ETP Hargreaves

## Overview
This component calculates the ETP using the Hargreaves method. It receives a CSV file with the data of the stations and the dates, and returns a CSV file with the ETP values for each station and date.

## Usage
Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then run the script with:
```sh
python main.py --help
```

## Test
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
docker build -t enbic2lab/water/etp_hargreaves:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/etp_hargreaves:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/etp_hargreaves:1.0.0 --filepath /mnt/shared/ETP_preprocessing.csv --delimiter ";"
```
>   - `--delimiter` is optional, if it is not declared, ";" will be used as default.
