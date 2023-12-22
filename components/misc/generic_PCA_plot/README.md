# Generic PCA plot

## Overview
This component creates a generic PCA plot from any csv file. It does a simple PCA on the data and plots the first two principal components.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_pca_plot:1.0.5 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_pca_plot:1.0.5 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_pca_plot:1.0.5 --filepath /mnt/shared/input.csv --delimiter ";" --target-column "column A" --title "My title" --x-label "My x label" --y-label "My y label" --color-list "red, blue, yellow" 
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--color-list` is optional, if not present or the number does not match the target values the colors will be the seaborn's default color palette ('tab10'). The colors must be separated by commas(',').
> `--title`, `--x-label` and `--y-label` are optional, by default they are the default values selected by seaborn.
