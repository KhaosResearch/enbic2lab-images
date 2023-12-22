# Preprocessing ETP

## Overview
This script expects a CSV with the following columns:
- Fecha
- TMAX
- TMIN
- Latitud

  
Using this information the script will retrive a CSV with the precipitation data for every station per date.

> :warning: **WARNING**: This component may take a long time to process data if the dataset imported is too big


> Component done by:
> - Irene Sánchez Jiménez (iresanjim@uma.es),
> - Irene Romero Granados (ireero99@uma.es)


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
docker build -t enbic2lab/water/preprocessing_etp:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/preprocessing_etp:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/preprocessing_etp:1.0.0 --filepath "/mnt/shared/input_etp.xlsx" --cte1 "37.59" --cte2 "0.01745" --kt "0.175" --output "/mnt/shared/"
```