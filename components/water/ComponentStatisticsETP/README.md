# LLU calculation

## Overview
This Python script calculates statistics (Max, Min, Mean, Median, Variance, Standard-Deviation, Variation-Coefficient, Asymmetry-Coefficient, Kurtosis) from selected variables.

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
Precipitación;
ETP Hargreaves;
LLU;
ESC;
INF

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
docker build -t enbic2lab/water/etp_statistics_component:1.0.1 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/etp_statistics_component:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/etp_statistics_component:1.0.1 --filepath /mnt/shared/input.csv --delimiter ";" --start-year 2008 --end-year 2011 --hydrological-year "True" --variables-list "TMAX,TMIN,Latitud,TMedia,Distancia Tierra-Sol,Declinación diaria en grados" --metrics-list "Max,Min,Mean,Median,Range" --output "/mnt/shared/output.csv"
```