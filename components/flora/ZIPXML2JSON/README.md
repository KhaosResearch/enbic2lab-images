# ZIPXML2JSON

## Overview

This script is responsible for transforming a ZIP file with several XML into a JSON file composed of flora inventories. The input XML files structure follows the following XMLSchema: http://biodiver.bio.ub.es/vegana/resources/schemas/ReleveTable1.2.xsd. And the output JSON file (`output.json`) with inventories follows the following structure:

```json
{
    "_id": None,
    "Date": None,
    "Authors": [],
    "Group": "Flora",
    "Project": None,
    "Community": None,
    "Community_Authors": [],
    "Community_Year": None,
    "Subcommunity": None,
    "Subcommunity_Authors": [],
    "Subcommunity_Year": None,
    "Location": None,
    "MGRS": None,
    "Natural_Site": None,
    "Lithology": None,
    "Coverage": None,
    "Altitude": None,
    "Plot_Slope": None,
    "Alt_Veg": None,
    "Plot_Area": None,
    "Plot_Orientation": None,
    "Ecology": None,
    "Species": [],
    "Pictures": [],
    "DataOrigin": "SIVIM"

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
docker build -t $REGISTRY/enbic2lab/flora/zipxml2json:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/zipxml2json:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/zipxml2json:1.0.1 --filepath "/mnt/shared/Inventarios_depurados.zip" --natural-site "Cado de Gata"
```