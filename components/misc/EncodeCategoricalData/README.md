# Encode Categorical Data

## Overview
This component encodes categorical data from a CSV file using ordinal encoding or one-hot encoding, depending on the number of unique values in the column. It is intended to make a quick preprocessing of the data if needed.

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
docker build -t $REGISTRY/enbic2lab/misc/encode_categorical_data:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/encode_categorical_data:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/encode_categorical_data:1.0.0 --filepath /mnt/shared/train.csv --delimiter ";" --exclude-columns "column A, column B"
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ";".
> `--exclude-columns` is optional, by default it is set to None. If specified, the columns names must be separated by a commas (,).
