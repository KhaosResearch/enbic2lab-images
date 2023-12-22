# Aemet Add Statistics

## Overview
Create a CSV File with extra columns based on statistics.

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
docker build -t enbic2lab/air/aemet_add_statistics:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/air/aemet_add_statistics:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/air/aemet_add_statistics:1.0.0 --filepath "mnt/shared/6155A_aemet_pollen_meteo_olea_data_updated_linear_interpolation.csv" --delimiter ";" --output /"mnt/shared/6155A_aemet_urtica_statistics.csv" --acum-list-attr "sol,prec,Hum_rel" --mm-list-attr "tmed,tmax,tmin,dir,velmedia,racha,sol,presMax,presMin,Index,prec,CALMA,Hum_rel,Vto_1,Vto_2,Vto_3,Vto_4"
```


