# Relation plot

## Overview
This component creates a generic Relation plot from any csv file indicating the columns to be analyzed and more columns to autmatically change size, hue and style to classify and show the relation between the two principal columns.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_relplot:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_relplot:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_relplot:1.0.0 --filepath /mnt/shared/input.csv --delimiter ";" --x-column "column A" --y-column "column B" --palette "Set1" --hue "column C" --size "column D" --style "column E" --kind "scatter" --col "column F" --row "column G"
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--palette` is optional, by default it is set to "tab10".
> `--kind` defines the type of the plot. It is optional, by default it is set to "scatter".
> `--col` defines a column to divide the plots in column. It is optional, by default it is set to None.
> `--row` defines a column to divide the plots in row. It is optional, by default it is set to None.
> `--size` defines a column to change the size of the points. It is optional, by default it is set to None.
> `--style` defines a column to change the style of the points. It is optional, by default it is set to None.
> `--hue` defines a column to change the color of the points. It is optional, by default it is set to None.
