# Correlation matrix heatmap

## Overview
This script receives the `correlation_matrix_heatmap.csv` file and plots the heatmap of the correlation matrix into a PDF file (`correlation_matrix_heatmap.pdf`).

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
docker build -t $REGISTRY/enbic2lab/soil/pca_heatmap:1.0.3 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directory, it can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/soil/pca_heatmap:1.0.3 --help
```

e.g.
```sh
<<<<<<< HEAD
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/pca_heatmap:1.0.3 --filepath "/mnt/shared/PCA_plot.csv" --delimiter ";"
=======
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/pca_heatmap:1.0.1 --filepath "/mnt/shared/PCA_plot.csv" --delimiter ";"
```
