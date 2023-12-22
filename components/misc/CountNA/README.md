## Count NA

## Overview
This component expects a CSV file and search in it for NAs and plots it in a PDF file. It will create a chart for each column. 


## Usage
Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then run the script with:
```sh
python main.py --help
```

## Test

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
docker build -t $REGISTRY/enbic2lab/misc/CountNA:1.0.1 .
```


### Run

Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/CountNA:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/CountNA:1.0.1 --filepath mnt/shared/input.csv --delimiter ";"
```
> The output path may be changed using the `--output-path` argument.