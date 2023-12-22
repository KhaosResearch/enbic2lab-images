# Violin plot

## Overview
This component creates a generic Violin plot from any csv file indicating the column to be analyzed and some more styling options.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_violinplot:1.0.3 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_violinplot:1.0.3 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_violinplot:1.0.3 --filepath /mnt/shared/input.csv --delimiter ";" --x-column "column A" --y-column "column B" --hue "column C" --palette "Set1" --title "My title" --orient "horizontal" --inner "box" --split True 
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--hue` is optional, by default it is set to None.
> `--palette` is optional, by default it is set to "tab10".
> `--title` is optional, by default it is set to None.
> `--orient` is optional, by default it is set to "vertical". Must be either "vertical" or "horizontal".
> `--inner` is optional, by default it is set to "box". Must be either "box", "quartile", "point", "stick", or "none".
> `--split` is optional, by default it is set to False. Must be either True or False. It will only be used if hue is present and is lower than 2.