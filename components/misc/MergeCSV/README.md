# Merge CSVs

## Overview

Merges the two input CSV files
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
docker build -t enbic2lab/misc/merge_csv:1.0.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/misc/merge_csv:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/misc/merge_csv:1.0.0 --filepath1 "mnt/shared/species_alcornocales.csv" --filepath2 "mnt/shared/species_cabo_de_gata.csv" --delimiter1 ";" --delimiter2 ";" --output "mnt/shared/output.csv"
```