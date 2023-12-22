# Data normalization

## Overview
This script expects a the CSV file from a previous component and normalizes it returning another normalized CSV (`DataNormalized.csv`)

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
docker build -t $REGISTRY/enbic2lab/soil/data_normalization:1.0.1 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directory, it can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/soil/data_normalization:1.0.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/data_normalization:1.0.1 --filepath "/mnt/shared/Data.csv" --delimiter ";"
```
> The output file path may be changed using the `--output-path` parameter.
> **Note**: A target column can be especified using the parameter `--target-column`. It is empty by default.
