# Station Comparison

## Overview
This component analyzes the precipitations data of 2 different stations from a CSV file. This CSV has an expected form like the following:

| DATE | STATION 1 | STATION 2 | ... | STATION N |
| ---- | --------- | --------- | --- | --------- |
| 01/01/1970 | 1.0 | 0.0 | ... | 0.0 |
| 02/01/1970 | 0.0 | 1343.0 | ... | 0.0 |
| ... | ... | ... | ... | ... |
| 31/12/2019 | 120.0 | 0.0 | ... | 3141.127 |
> NOTE: It is important that the Date column has the same name as in the example.

This script will generate an interactive scatter plot with its regression line and will write it into a HTML file.

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
docker build -t $REGISTRY/enbic2lab/water/station_comparison:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/station_comparison:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/station_comparison:1.0.2 --filepath /mnt/shared/precipitations.csv --stationA "STATION 1" --stationB "STATION 2" --delimiter ";"
```
> NOTE: `--delimiter` is optional, by default it is set to ";".