# Random Forest

## Overview
This component trains a Random Forest model on a dataset given and outputs the model as a ONNX file, some metrics plots and the plot of the forest itself.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_classification_randomforest:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_classification_randomforest:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_classification_randomforest:1.0.0 --filepath-train /mnt/shared/train.csv --filepath-test /mnt/shared/test.csv --delimiter ";" --target-column "column A"
```
> The output file path may be changed using the `--output-path` argument.
> `--target-column` is **compulsory**.
> `--delimiter` is optional, by default it is set to ";".
