# EXCEL2JSON

## Overview

This script takes as an entrance an XLSX file with flora inventory data and transforms it into a JSON (`output.json`) file with its content. The structure of the XLSX input file is as follows:

|  | A | B | C | D |
|---|---|---|---|---|
| Metadata - 1 |||||
| Metadata - 2 |||||
| Metadata - 3 |||||
| Metadata - 4 |||||
|  |||||
|  | INVENTARIO Nº | 0 | 0 | 0 |
|  | Orientación| N | E | S |
|  | Inclinación (º)  | 0 | 0 | 0 |
|  | Altitud (m)| 0 | 0 | 0 |
|  | Cobertura (%) | 0 | 0 | 0 |
|  | Área (m 2) | 0 | 0 | 0 |
|  | Litología  | Lit-1 | Lit-2 | Lit-3 |
|  | Altura vegetación (cm) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|  |  |||
|  | Anagallis monelli| . | . | + |
|  | Anthyllis vulneraria subsp. maura  | + | . | . |
|  | Aphyllanthes monspeliensis| . | + | . |
|  | Arbutus unedo | . | . | . |
|  | Aristolochia baetica| . | . | . |
|  | Aristolochia longa  | . | + | . |
|  | Arum italicum subsp. italicum| + | . | . |
|  |  |||
| Localidad | Loc-1 | Loc-2 | Loc-3 | Loc-4 |
| UTM | Utm-1  | Utm-2 | Utm-3 | Utm-4 |

And generates a JSON file with the following fields:

```json
{
    "_id": "",
    "Date": "",
    "Authors": [],
    "Group": "Flora",
    "Project": "",
    "Community": "",
    "Community_Authors": [],
    "Community_Year": "",
    "Subcommunity": "",
    "Subcommunity_Authors": [],
    "Subcommunity_Year": "",
    "Location": "",
    "MGRS": "",
    "Natural_Site": "",
    "Lithology": "",
    "Coverage": "",
    "Altitude": "",
    "Plot_Slope": "",
    "Alt_Veg": "",
    "Plot_Area": "",
    "Plot_Orientation": "",
    "Ecology": "",
    "Species": [],
    "Pictures": [],
    "DataOrigin":""
}
```

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

Install the requirements for testing:

```sh
python -m pip install -r requirements-dev.txt
```

Run the tests with:

```sh
python test_main.py
```

## Docker

### Build

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/flora/excel2json:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/excel2json:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/excel2json:1.0.1 --filepath "/mnt/shared/0.Zara 9. Asparago albi-Rhamnetum oleidis rhamnetosum oleidis.xlsx" --natural-site "Alcornocales" --mgrs-zone "30S"
```
