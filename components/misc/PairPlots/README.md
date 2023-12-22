# Pair plot

## Overview
This component creates a generic Pair chart plot from any csv file indicating the type of graph to be plotted and some customizable parameters.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_pairplot:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_pairplot:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_pairplot:1.0.0 --filepath /mnt/shared/input.csv --delimiter ";" --kind "scatter" --diag-kind "auto" --title "My title"  --hue "column C" --palette "Set2" 
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--kind` is optional, by default it is set to "scatter". It can be set to "scatter", "reg", "kde", "hist".
> `--diag-kind` is optional, by default it is set to "auto". It can be set to "auto", "hist", "kde", "none".
> `--hue` is optional, by default it is set to None.
> `--palette` is optional, by default it is set to seaborn's default 'tab10'.
> `--title` is optional, by default it is None.
