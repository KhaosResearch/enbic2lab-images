# Upload to DB

## Overview

This component upload JSON file to MongoDB

### Input
input.json

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
python test_main.py
```

## Docker

### Build

Build the image with:

```sh
docker build -t enbic2lab/air/upload2db:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/upload2db:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/upload2db:1.0.0  --filepath "mnt/shared/6155A_aemet_pollen_meteo_platanus_data_updated_linear_interpolation_statistics.json" --user "user" --password "password" --path "mongodb://0.0.0.0:0" --collection "collection" --database "database"
```