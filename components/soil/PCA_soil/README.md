# PCA Components

## Overview
This script expects the normalized CSV file from a previous component and does a PCA to it returning four different CSV 
files with information about it like the correlation matrix (`correlation_matrix_heatmap.csv`), covariance matrix (`covariance_matrix.csv`),
the PCA components values (`PCA_plot.csv`) and the scree plot (`scree_plot.csv`).

This component unifies `PCA_component` and `PCA_variance` into one only component that allows user to apply the logic of one or the other.

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
docker build -t $REGISTRY/enbic2lab/soil/pca_soil:1.0.2 .
```

### Run
Run the image with (assuming that the CSV file is in the `data` folder from the current directory, it can be changed as desired):

```sh
docker run --rm $REGISTRY/enbic2lab/soil/pca_soil:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/pca_soil:1.0.2 --filepath "/mnt/shared/DataNormalized.csv" --delimiter ";" --number-components 5
```
> **NOTE**: You can change the output path files using `--output-path`.
> **NOTE**: You can select the number of components manually using `--number-components` or the variance expected using `--variance-expected`. Number of components have priority over variance. If both are missing a default variance of 75 will be used to calculate the number of components.
> **NOTE 2**: A target column can be especified using the parameter `--target-column`. It is empty by default.
> **NOTE 3**: `--delimiter` is optional and by default is set to ";".
