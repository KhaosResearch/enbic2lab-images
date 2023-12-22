# Delete NA

## Overview

This script is a generic NA dropper, which means that it can receive a CSV with tabular data in which it will search for NAs and delete its row or column. This component only deletes them and is not intended to interpolate or generate new data. You may select how do you want to delete the NAs between 'column', 'row' and 'both'. If 'column' is selected it will delete only the columns that has all its data missing, however if 'row' is chosen, whenever a NA is found its row is deleted. If 'both' is chosen, the component will do both 'column' and 'row' filtration.

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
docker build -t $REGISTRY/enbic2lab/misc/delete_na:1.0.1 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/delete_na:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/delete_na:1.0.1 --filepath "/mnt/shared/inputData.csv" --delimiter ";" --delete-option both
```
> Output file path may be changed using `--output-path` argument.
> **Note**: By default `both` is selected for `--delete-option`.