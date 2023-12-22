# Monthly precipitation plot

## Overview
This Python script generates interactive visualizations of precipitation data from an input CSV file containing relevant meteorological information. 

Expects a CSV:

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
docker build -t enbic2lab/water/temperature_plot_component:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm enbic2lab/water/temperature_plot_component:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/temperature_plot_component:1.0.0 --filepath mnt/shared/ComponentINF.csv --delimiter ";" --mode "both"
```