# Load Inventory

## Overview

This Python script is designed to extract inventory flora data from a MongoDB collection and export it to a CSV file. The script allows you to filter the data based on various criteria such as date, community, location, and more. It offers flexible filtering options to retrieve specific inventory records that meet your requirements.

The MongoDB collection structure should be as follows:

```json
{
    "_id": "", 
    "Alt_Veg": 0, 
    "Altitude": 0, 
    "Authors": [""], 
    "Community": "", 
    "Community_Authors": [""], 
    "Community_Year": 0, 
    "Coverage": 0, 
    "Date": "", 
    "Ecology": "", 
    "Group": "", 
    "Latitude": 0, 
    "Lithology": "",
    "Location": "",
    "Longitude": 0,
    "Natural_Site": "",
    "Pictures": [""],
    "Plot_Area": 0,
    "Plot_Orientation": "",
    "Plot_Slope": "",
    "Project": "",
    "Species": [
        {
            "Name": "",
            "Ind": ""
        },
    ],
    "Subcommunity": "",
    "Subcommunity_Authors": [""],
    "Subcommunity_Year": 0,
    "MGRS": "",
    "UTM": ""
}
```

And returns a table (`output.csv`) with the inventory records.

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
python -m pytest
```

## Docker

### Build

Build the image with:

```sh
source .env
docker build -t $REGISTRY/enbic2lab/flora/load_inventory:1.0.1 \
            --build-arg mongo_host=${MONGO_HOST} \
            --build-arg mongo_username=${MONGO_USERNAME} \
            --build-arg mongo_access_key=${MONGO_ACCESS_KEY} \
            --build-arg mongo_database=${MONGO_DATABASE} .
```

### Run

Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/flora/load_inventory:1.0.1
--help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/load_inventory:1.0.1 --natural-site "Cabo de Gata" --location "Salinas de Cabo de Gata, Almería"
```