# Aemet download data

## Overview
Download meteorological data from AEMET

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
docker build -t enbic2lab/air/aemet_download_data:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/air/aemet_download_data:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/aemet_download_data:1.0.0 --aemet-api-key "" --start-date "1991-05-11" --end-date "2021-09-30" --station "6155A"  --delimiter ";" --output "/mnt/shared/output.csv"
```
