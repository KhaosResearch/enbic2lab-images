# KMeans Clustering

## Overview
This component trains a KMeans model on a dataset given and outputs the model as a ONNX file and the metrics plots.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_clustering_kmeans:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_clustering_kmeans:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_clustering_kmeans:1.0.2 --filepath-train /mnt/shared/train.csv --filepath-test /mnt/shared/test.csv --delimiter ";" --target-column "column A" --n-clusters 3
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ";".
> `--target-column` is optional, by default it is set to None.
> `--n-clusters` is optional, it may be "auto" or an int, by default is "auto".
