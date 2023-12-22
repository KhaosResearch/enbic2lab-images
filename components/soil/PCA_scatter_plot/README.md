# PCA scatter plot

## Overview
This script receives the `PCA_plot.csv` file and plots 2 of the Principal Components of it into a file (`PCA_plot.pdf`).

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
docker build -t $REGISTRY/enbic2lab/soil/pca_scatter_plot:1.1.3 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directory, it can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/soil/pca_scatter_plot:1.1.3 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/pca_scatter_plot:1.1.3 --filepath "/mnt/shared/PCA_plot.csv" --delimiter ";" --x-axis PC1 --y-axis PC2 --color-list red yellow
```
> **Note**: `--delimiter` is optional, the default is `;`.
    > `--target-column` is optional, the default is `None`.
    > `--output-path` is optional, the default is `/mnt/shared`.
