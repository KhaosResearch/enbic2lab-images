# Kriging interpolation 3D

## Overview

This script expects several files:

* A zip file containing a shapefile with at least one column with values to interpolate.
* A Digital Elevation Model (DEM) file in tif format.

And returns a plot of the interpolated values (`output.png`) and a CSV with the raw data (`output.csv`).

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

This script does not have a test because the main algorithm is a taken from the `pykrige==1.7.1` library, and as such is expected to work. As testing this component entails a reference shapefile, DEM and to manually check the output of the interpolation.

## Docker

### Build

Build the image with:

```sh
docker build -t enbic2lab/water/kriging_interpolation:1.0.0 .
```

### Run

Run the image with (assuming that the input files are in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/water/kriging_interpolation:1.0.0 --help

```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/water/kriging_interpolation:1.0.0 --shp-path /mnt/shared/TEMPERATURA.zip --dem-path /mnt/shared/dem.tif --column-name T --use-shp-height True --grid-size 100 --output /mnt/shared/
```
