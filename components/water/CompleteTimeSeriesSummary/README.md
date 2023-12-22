# Plot Highlight Summary

## Overview
This component expects two CSV files with the information about the completion of the time series data of the target station. It will show the information and highlight the added values in an HTML table. The CSV files must be in the following format:

| DATE | STATION-NAME | 
| ---- | --------- |
| 1993-11-02 | 0.0 |
| 1993-11-03 | 30.651 |
| ... | ... | ... | ... |
| 2019-12-31 | 14.971 |
> NOTE: It is important that the DATE column has the same name in the given CSV files.

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
docker build -t $REGISTRY/enbic2lab/water/complete_timeseries_summary:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/complete_timeseries_summary:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/complete_timeseries_summary:1.0.2 --filepath-completed /mnt/shared/TargetCompleted.csv --filepath-replaced /mnt/shared/CompletedData.csv --color green --delimiter ";"
```
> The output file path may be changed using the `--output-path` argument.
> NOTE: `--color` is optional, by default it is set to "cyan".
> NOTE: `--delimiter` is optional, by default it is set to ";".