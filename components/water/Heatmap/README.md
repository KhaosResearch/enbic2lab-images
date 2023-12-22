# Heatmap

## Overview
This component generates a heatmap from precipitation data stored in a CSV file. It takes input parameters such as the file path, date and station column names, and a color palette. The CSV input expected shuould be similar to:

|Hidrologic Year | Station | Year Mean | Year Maximum | Year minimum | Year Collected Data | Year Empty Data | Year Collected Data (Percentage) | Year Empty Data (Percentage) | Sum of the Year|
|----------------|---------|-----------|--------------|--------------|---------------------|-----------------|---------------------------------|-----------------------------|----------------|
|1902/1903 | CASTAÑO DEL ROBLEDO | 1.2 | 20.0 | 0.0 | 150 | 215 | 41.0 | 59.0 | 80.0 |
|1903/1904 | JABUGO | 1.2 | 20.0 | 0.0 | 150 | 215 | 41.0 | 59.0 | 80.0 |
|1904/1905 | CASTAÑO DEL ROBLEDO | 1.2 | 20.0 | 0.0 | 150 | 215 | 41.0 | 59.0 | 80.0 |
> Note: This data is not real, it is just an example.
> Note 2: The column names will be passed as parameters.

The code processes the data, pivots it for the heatmap, and styles the visualization. The resulting heatmap is saved as a PNG image. 

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
docker build -t $REGISTRY/enbic2lab/water/heatmap:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/water/heatmap:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/water/heatmap:1.0.0 --filepath /mnt/shared/StatiscalData.csv --date-column "Hidrologic Year" --station-column Station --percentage-column "Year Collected Data (Percentage)" --palette RdYlBu_r --delimiter ";"
```
> `--percentage-column` expects the name of the column that contains the percentage of collected data.

> **Note**: Some parameters are optional:
>   - `--delimiter` is optional, if it is not declared, ";" will be used as default.
>   - `--palette` is optional, its default value is "RdYlBu_r". It may receive any of the palettes available in: ["rocket", "mako", "flare", "crest", "rocket_r", "mako_r", "flare_r", "crest_r", "viridis", "plasma", "inferno", "magma", "cividis", "viridis_r", "plasma_r", "inferno_r", "magma_r", "cividis_r", "Greys", "Reds", "Greens", "Blues", "Oranges", "Purples", "BuGn", "BuPu", "GnBu", "OrRd", "PuBu", "PuRd", "RdPu", "YlGn", "PuBuGn", "YlGnBu", "YlOrBr", "YlOrRd", "Greys_r", "Reds_r", "Greens_r", "Blues_r", "Oranges_r", "Purples_r", "BuGn_r", "BuPu_r", "GnBu_r", "OrRd_r", "PuBu_r", "PuRd_r", "RdPu_r", "YlGn_r", "PuBuGn_r", "YlGnBu_r", "YlOrBr_r",             "YlOrRd_r", "Greys_d", "Reds_d", "Greens_d", "Blues_d", "Oranges_d", "Purples_d", "BuGn_d", "BuPu_d", "GnBu_d","OrRd_d", "PuBu_d", "PuRd_d", "RdPu_d", "YlGn_d", "PuBuGn_d", "YlGnBu_d", "YlOrBr_d", "YlOrRd_d", "vlag", "vlag_r", "icefire", "icefire_r", "coolwarm", "bwr", "sismic", "RdBu", "RdGy", "PRGn", "PiYG", "BrBG", "RdYlBu", "RdYlGn", "Spectral", "RdBu_r", "RdGy_r", "PRGn_r", "PiYG_r", "BrBG_r", "RdYlBu_r", "RdYlGn_r", "Spectral_r"]. For further information see: [https://seaborn.pydata.org/tutorial/color_palettes.html](https://seaborn.pydata.org/tutorial/color_palettes.html)
> - `--date-column` is optional, its default value is "Hidrologic Year".
> - `--station-column` is optional, its default value is "Station".