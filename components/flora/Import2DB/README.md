# Import JSON to DB

## Overview

This script expects a JSON file with the following structure:

```json
[{  "_id": "", 
    "Date": null, 
    "Authors": [], 
    "Group": "", 
    "Project": null, 
    "Community": "", 
    "Community_Authors": [""], 
    "Community_Year": 0, 
    "Subcommunity": null, 
    "Subcommunity_Authors": [], 
    "Subcommunity_Year": null, 
    "Location": "", 
    "MGRS": null, 
    "Natural_Park": "", 
    "Lithology": null, 
    "Coverage": null, 
    "Altitude": 0, 
    "Plot_Slope": null, 
    "Alt_Veg": null, 
    "Plot_Area": 0, 
    "Plot_Orientation": "", 
    "Ecology": null, 
    "Species": [{"Name": "", "Ind": ""}], 
    "Pictures": []
}]
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

## Docker

### Build

Set the required environment variables in the `Dockerfile`.

Then, build the image with:

```sh
docker build -t enbic2lab/flora/import2db:1.0.0 .
```

### Run

Run the image with (assuming that the JSON file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/flora/import2db:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/flora/import2db:1.0.0 --filepath "inventory.json"
```
