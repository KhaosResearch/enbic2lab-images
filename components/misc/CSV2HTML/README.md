# CSV2HTML

## Overview

This script is a generic format converter. It allows you to transform any CSV into an HTML table. The script assumes the existence of a header on the first line of the CSV. Here is a possible entry example:

```csv
A,B,C,D
1,4,3,6
4,8,5,2
9,0,3,7
```

For which the script generates an HTML file with the same table with a predefined style (`output.html`)

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
docker build -t $REGISTRY/enbic2lab/misc/csv2html:1.1.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/csv2html:1.1.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/csv2html:1.1.1 --input "/mnt/shared/StatisticalData_correct.csv" --delimiter ","
```

> The output file path may be changed using the `--output-path` option.