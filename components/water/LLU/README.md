# LLU calculation

## Overview
This Python script calculates the Liquid Limit Update (LLU) using an input CSV file containing essential meteorological data. The script utilizes parameters such as useful rainfall (ru) and the name of the Evapotranspiration (ETP) variable to perform the calculation.

Expected CSV file:
Fecha;
TMAX;
TMIN;
TMedia;
Latitud;
Día juliano;
Distancia Tierra-Sol;
Declinación diaria en grados;
Latitud RAD;
Declinación RAD;
(menos)Tangente;
Tangente declinación;
Multiplicación;
Angulo horario (radianes);
Angulo horario (Grados);
CTE1;
CTE2;
Seno latitud;
Seno declinación;
Coseno latitud;
Coseno declinación;
Seno ángulo horario;
tmax-tmin^0,5;
tmax-tmin^0,99;
tmax-tmin^0,75;
tmax-tmin^0,25;
tmax-tmin^0,01;
KT;
Ro;
Ro EXTRATERRESTRE mm/dia;
Rs;
Ravanazzi;
ETP Hargreaves;
Precipitación

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
docker build -t enbic2lab/water/llu_component:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/llu_component:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/llu_component:1.0.0 --filepath /mnt/shared/ETP_Hargreaves_complete.csv --delimiter ";" --ru "50" --etp_name "Hargreaves"
```