# Aemet Create Stations Dataset
## Overview
Create a CSV File with data about an attribute from Aemet for differents stations
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
docker build -t enbic2lab/air/create_stations_dataset:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/air/create_stations_dataset:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/create_stations_dataset:1.0.0 --filepath "/mnt/shared/stations_weather_attributes.json" --output "/mnt/shared/output.csv" --attribute "prec" --delimiter ";" 
```


