# Inventory Statistics

## Overview

This Python script reads a dataset, preprocesses it, and applies the Apriori algorithm to find frequent itemsets and association rules based on user-defined support and confidence thresholds. It then saves the results in CSV files

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
docker build -t $REGISTRY/enbic2lab/flora/fidelity_species_index:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/fidelity_species_index:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/fidelity_species_index:1.0.1 --filepath "/mnt/shared/inventory_transformation.csv" --delimiter ";" --min_support 0.05 --min_threshold 0.85
```
