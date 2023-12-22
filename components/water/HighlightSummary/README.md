# Plot Highlight Summary

## Overview
This component expects a CSV file with the precipitations data of several stations. This CSV has an expected form like the following:

| Hidrologic Year | Station | ... | Sum of the Year |
| ---- | --------- | --------- | --- | --------- |
| 1902/1903 | STATION 1 | ... | 10.0 |
| 1905/1906 | STATION 1 | ... | 0.0 |
| ... | ... | ... | ... | ... |
| 2022/2023 | STATION N | ... | 3141.127 |
> NOTE: It is important that the columns of the example appear in the CSV given.

It will display the information given plus statistical information calculated about the data, highlighting the high and low precipitation years.

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
docker build -t $REGISTRY/enbic2lab/water/plot_highlight_summary:1.0.4 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/plot_highlight_summary:1.0.4 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/plot_highlight_summary:1.0.4 --filepath /mnt/shared/StatisticalData.csv --delimiter ";"
```
> The output path may be changed using the `--output-path` argument.
> NOTE: `--delimiter` is optional, by default it is set to ";".