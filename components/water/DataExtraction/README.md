# Data Extraction

## Overview
This script expects a CSV with the following shape:
| DATE | STATION 1 | STATION 2 | ... | STATION N |
|------|-----------|-----------|-----|-----------|
| 1/1/2019 | 0.0 | 0.0 | ... | 0.0 |
| 2/1/2019 | 2.10 | 0.0 | ... | 0.0 |
| ... | ... | ... | ... | ... |
| 31/12/2019 | 0.0 | 0.0 | ... | 12.0 |
| 1/1/2020 | 0.0 | 0.0 | ... | 0.0 |
| ... | ... | ... | ... | ... |
| 31/12/2020 | 45.0 | 0.0 | ... | 97.2 |
| ... | ... | ... | ... | ... |

Using this information the script will retrive another CSV with some statiscal information about the precipitation in the stations, the shape of the output CSV is the following:

| Hidrologic Year | Station | Year Mean | Year Maximum | Year minimum | Year Collected Data | Year Empty Data | Year Collected Data (Percentage) | Year Empty Data (Percentage) | Sum of the Year |
|------|-----------|-----------|-----|-----------|-----------|-----------|-----------|-----------|-----------|
| 1902/1903 | STATION 1 |  |  |  | 0 | 365 | 0.0 | 100.0 |  |
| 1903/1904 | STATION 1 | 1.925 | 66.2 | 0.0 | 0 | 366 | 0.0 | 100.0 | 702.6 | |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1902/1903 | STATION 2 |  |  |  | 0 | 365 | 0.0 | 100.0 | |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 1902/1903 | STATION N |  |  |  | 0 | 365 | 0.0 | 100.0 | |
| ... | STATION N | ... | ... | ... | ... | ... | ... | ... | ... |

> **IMPORTANT**:heavy_exclamation_mark:: The column `DATE` must have the same name as the example.

> Component done by:
> - Irene Sánchez Jiménez (iresanjim@uma.es),
> - Juan Carlos Ruiz Ruiz (juancaruru@uma.es)


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
docker build -t $REGISTRY/enbic2lab/water/data_extraction:1.0.1 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/data_extraction:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/data_extraction:1.0.1 --filepath mnt/shared/precipitationTimeSeries.csv --delimiter ";"
```
> Output file path may be changed using `--output-path` argument
> **Note**: `--delimiter` is optional, if it is not declared, ";" will be used as default