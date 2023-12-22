# SKLearn Predictor

## Overview
This component receives a SKLearn model in ONNX format and makes a prediction on a given dataset.

> :exclamation:**IMPORTANT**: The input dataset must be in the **same format** and have the **same columns** as the dataset used to train the model.

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
docker build -t $REGISTRY/enbic2lab/misc/sklearn_predictor:1.0.1 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/sklearn_predictor:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/sklearn_predictor:1.0.1 --filepath-model /mnt/shared/model.onnx --filepath-data /mnt/shared/predict.csv --delimiter ";"
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ";".
