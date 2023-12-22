# Precipitation matrix transform

## Overview
This script expects a XLSX file with the following columns:
- INDICATIVO
- AÑO
- MES
- NOMBRE
- ALTITUD
- C_X
- C_Y
- NOM_PROV
- LONGITUD
- LATITUD
- TMAX1
- ...
- TMAX31
- TMIN1
- ...
- TMIN31
  
Using this information the script will retrive 2 CSV files with the maximum and minimum temperature for each day of the year.

> :warning: **WARNING**: This component may take a long time to process data if the dataset imported is too big


> Component done by:
> - Irene SÃ¡nchez Jiménez (iresanjim@uma.es),
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
docker build -t $REGISTRY/enbic2lab/water/temperature_matrix_transformation:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/temperature_matrix_transformation:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/temperature_matrix_transformation:1.0.2 --filepath mnt/shared/temperature.xlsx --delimiter ";"
```
> The output path may be changed using the `--output-path` argument.
> **Note**: `--delimiter` is optional, if it is not declared, ";" will be used as default