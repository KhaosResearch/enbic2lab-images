# PCA variance plot

## Overview
This script receives the `scree_plot.csv` file and plots the variance of all the possible principal components into a PDF file(`scree_plot.pdf`).

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
docker build -t $REGISTRY/enbic2lab/soil/pca_variance_plot:1.1.1 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directory, it can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/soil/pca_variance_plot:1.1.1 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/pca_variance_plot:1.1.1 --filepath "/mnt/shared/scree_plot.csv" --delimiter ";"
```
> **NOTE**: Output file path may be changed using the `--output-path` argument.
