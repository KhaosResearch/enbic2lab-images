# Precipitation matrix transform

## Overview
This script expects a CSV with the following columns:
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
- P1
- P2
- P3
- P4
- P5
- P6
- P7
- P8
- P9
- P10
- P11
- P12
- P13
- P14
- P15
- P16
- P17
- P18
- P19
- P20
- P21
- P22
- P23
- P24
- P25
- P26
- P27
- P28
- P29
- P30
- P31
  
Using this information the script will retrive another CSV with the precipitation data for every station per date.

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
docker build -t $REGISTRY/enbic2lab/water/precipitation_matrix_transformation:1.0.4 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/precipitation_matrix_transformation:1.0.4 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/precipitation_matrix_transformation:1.0.4 --filepath mnt/shared/precipitation.csv --delimiter ";"
```
> **Note**: `--delimiter` is optional, if it is not declared, ";" will be used as default