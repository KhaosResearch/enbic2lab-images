# Clustermap

## Overview
This component generates a clustermap from precipitation or temperature data stored in a CSV file. It takes from the input CSV the Station, the Date and the Square columns, this last one may be "Sum of the Year" or "Year Mean", for Precipitation and Temperature data, respectively.

It returns a PNG image with the resultant clustermap.
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
docker build -t $REGISTRY/enbic2lab/water/clustermap:1.0.1 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/clustermap:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/clustermap:1.0.1 --filepath /mnt/shared/StatiscalData.csv --date-column "Hidrologic Year" --station-column Station --square-column "Sum of the Year" --palette RdYlBu_r --delimiter ";" --filter-row --no-drop-na
```
> The output file path may be changed using the `--output-path` parameter.
> `--square-column` expects the name of the column that contains the clusterization data, "Sum of the Year" or "Year Mean".

> `--filter-row` or `--filter-colum` are used to select wether to do the clusterization using rows or columns. If one of them is not present `--filter-row` is used by default. 
> `--no-drop-na` or `--drop-na` are used to replace the NA values with the mean of that column or to delete every row with NAs in it, respectively. If they are not present, `--no-drop-na` is used by default.

> **Note**: Some parameters are optional:
>   - `--delimiter` is optional, if it is not declared, ";" will be used as default.
>   - `--palette` is optional, its default value is "RdYlBu_r". It may receive any of the palettes available in: ["rocket", "mako", "flare", "crest", "rocket_r", "mako_r", "flare_r", "crest_r", "viridis", "plasma", "inferno", "magma", "cividis", "viridis_r", "plasma_r", "inferno_r", "magma_r", "cividis_r", "Greys", "Reds", "Greens", "Blues", "Oranges", "Purples", "BuGn", "BuPu", "GnBu", "OrRd", "PuBu", "PuRd", "RdPu", "YlGn", "PuBuGn", "YlGnBu", "YlOrBr", "YlOrRd", "Greys_r", "Reds_r", "Greens_r", "Blues_r", "Oranges_r", "Purples_r", "BuGn_r", "BuPu_r", "GnBu_r", "OrRd_r", "PuBu_r", "PuRd_r", "RdPu_r", "YlGn_r", "PuBuGn_r", "YlGnBu_r", "YlOrBr_r",             "YlOrRd_r", "Greys_d", "Reds_d", "Greens_d", "Blues_d", "Oranges_d", "Purples_d", "BuGn_d", "BuPu_d", "GnBu_d","OrRd_d", "PuBu_d", "PuRd_d", "RdPu_d", "YlGn_d", "PuBuGn_d", "YlGnBu_d", "YlOrBr_d", "YlOrRd_d", "vlag", "vlag_r", "icefire", "icefire_r", "coolwarm", "bwr", "sismic", "RdBu", "RdGy", "PRGn", "PiYG", "BrBG", "RdYlBu", "RdYlGn", "Spectral", "RdBu_r", "RdGy_r", "PRGn_r", "PiYG_r", "BrBG_r", "RdYlBu_r", "RdYlGn_r", "Spectral_r"]. For further information see: [https://seaborn.pydata.org/tutorial/color_palettes.html](https://seaborn.pydata.org/tutorial/color_palettes.html)
> - `--date-column` is optional, its default value is "Hidrologic Year".
> - `--station-column` is optional, its default value is "Station".