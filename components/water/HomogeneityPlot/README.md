# Homogeneity Plot

## Overview
This component analyzes the precipitations or the temperature data of an unique stations from a time series CSV file. This CSV has an expected form like the following:

| DATE | STATION |
| ---- | --------- |
| 01/01/1970 | 1.0 |
| 02/01/1970 | 0.0 |
| ... | ... |
| 31/12/2019 | 120.0 |
> NOTE: It is important that the Date column has the same name as in the example.

It will also expect another CSV file with the homogeneity tests data. This CSV has an expected form like the following:

|  | TEST 1 | ... | TEST N |
| ---- | --------- | --------- | --------- |
| Homogeneity | True | ... | False |
| Change Point Location | 1995-10-25 | ... | 2004-01-14 |
| P-value | 0.0040 | ... | 0.4550 |
| Maximum test Statistics | 23131.0 | ... | 0.0 |
| Average between change point | mean(mu1=2.3554, mu2=2.3554) | ... | mean(mu1=2.3554, mu2=2.3554) |
> The available tests are: "Pettit Test", "SNHT Test" and "Buishand Test".

Receiving both files, the component will plot the time series of the station and the homogeneity tests results. The plot will be saved in the output directory as an HTML file.

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
docker build -t $REGISTRY/enbic2lab/water/homogeneity_plot:1.0.1 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/homogeneity_plot:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/homogeneity_plot:1.0.1 --filepath-data /mnt/shared/TargetCompleted.csv --filepath-homogeneity /mnt/shared/HomogeneityTests.csv --data-type precipitation --criteria "Buishand Test" --delimiter ";"
```
> NOTE: `--delimiter` is optional, by default it is set to ";".
> NOTE: `--data-type` only accepts "precipitation" or "temperature".
> NOTE: `--criteria` only accepts "Pettit Test", "SNHT Test" or "Buishand Test". By default it is set to "Pettit Test". 