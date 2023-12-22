# XLSX2CSV

## Overview

This script is a generic format converter. It allows you to transform any XLSX file into a CSV table. The script lets you choose wether the XLSX has a header writen or not and the delimiter to use in the CSV output file (`output.csv`).

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
docker build -t $REGISTRY/enbic2lab/misc/xlsx2csv:1.0.1 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/xlsx2csv:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/xlsx2csv:1.0.1 --filepath "/mnt/shared/inputData.xlsx" --delimiter ";" --header true
```
> Output file path may be changed using the `--output-path` argument.
