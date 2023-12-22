# Update Dataset

## Overview

Update a CSV main file using data from another CSV aux file.

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
docker build -t enbic2lab/misc/update_dataset:1.0.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/misc/update_dataset:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/misc/update_dataset:1.0.0 --first-file "mnt/shared/6155A_aemet_pollen_meteo_platanus_data_split.csv" --second-file "mnt/shared/6155A_completed.csv" --col-first-file 'prec' --col-second-file '6155A' --name-column-date-first-file "fecha" --name-column-date-second-file "DATE" --delimiter-first-file ";" --delimiter-second-file ";" --output "/mnt/shared/6155A_aemet_pollen_meteo_urtica_data_updated.csv"
```