# Dataframe Mean Interpolation

## Overview
Fill Nan values using column mean interpolation by range.
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
docker build -t enbic2lab/air/dataframe_mean_interpolation:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/air/dataframe_mean_interpolation:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/dataframe_mean_interpolation:1.0.0 --filepath "/mnt/shared/6155A_aemet_pollen_meteo_urtica_data_updated.csv" --delimiter ";" --date-column "fecha" --initial-year "1991" --final-year "2021" --output "/mnt/shared/6155A_aemet_pollen_meteo_olea_data_updated_processed"
```


