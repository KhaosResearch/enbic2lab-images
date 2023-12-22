# Plot dendrogram 

## Overview

This script takes care of generates a hierarchical clustering dendrogram (`output.pdf`) based on the given data. The input CSV requires a column for each species and a row for each sample. An example of this input CSV could be:

```csv
;S1;S2;S3
M1;0.0;0.2;0.0
M2;0.0;0.0;0.3
M3;0.1;0.0;0.0
```

## Usage

Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then, run the script with:

```sh
python main.py --help
```

## Tests

Install the requirements for testing:

```sh
python -m pip install -r requirements-dev.txt
```

Run the tests with:

```sh
python test_main.py
```

## Docker

### Build

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/flora/plot_dendrogram:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/plot_dendrogram:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/plot_dendrogram:1.0.1 --filepath "/mnt/shared/clear_flora.csv" --delimiter ";" --metrdendrogram euclidean --methdendrogram ward --oriendendrogram top
```









