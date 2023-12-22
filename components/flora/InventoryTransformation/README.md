# Inventory Statistics

## Overview

This script performs an inventory data transformation using the Python programming language. It reads a CSV file, transposes it, and then applies various data transformations to the columns. Finally, it saves the transformed data to a new CSV file.

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
docker build -t $REGISTRY/enbic2lab/flora/inventory_transformation:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/inventory_transformation:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/inventory_transformation:1.0.1 --filepath "/mnt/shared/inventories.csv" --delimiter ";"
```
