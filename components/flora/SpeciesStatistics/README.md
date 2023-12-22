# Species Statistics

## Overview

This Python script reads species data from an input CSV file, removes specific permanent rows from the data, and calculates statistics for each species, including the count of occurrences and the average coverage percentage. It categorizes the coverage percentages into ranges and computes the frequency of each species. Finally, it saves the computed statistics in a new CSV file. The script takes input file path, delimiter, and output file path as command-line arguments, making it a flexible tool for analyzing and summarizing species-related data.

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
docker build -t $REGISTRY/enbic2lab/flora/species_statistics:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/species_statistics:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/species_statistics:1.0.1 --filepath "/mnt/shared/inventory_transformation.csv" --delimiter ";"
```
