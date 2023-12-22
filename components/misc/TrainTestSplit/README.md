# Train Test Splitter

## Overview
This component receives a CSV dataframe and splits it into prediction, training and test sets.

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
docker build -t $REGISTRY/enbic2lab/misc/train_test_split:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/train_test_split:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/train_test_split:1.0.2 --filepath /mnt/shared/input.csv --delimiter ";" --target-column "column A" --predict-split 0.1 --train-split 0.8
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ";".
> `--target-column` is optional, by default it is set to None.
> `--predict-split` is optional, by default it is set to 0.1.
> `--train-split` is optional, by default it is set to 0.8.
