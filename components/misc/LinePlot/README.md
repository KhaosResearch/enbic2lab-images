# Line plot

## Overview
This component creates a generic Line chart plot from any csv file indicating the columns of study to be plotted and some customizable parameters, such us the hue or the style columns.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_lineplot:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_lineplot:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_lineplot:1.0.2 --filepath /mnt/shared/input.csv --delimiter ";" --x-column "column A" --y-column "column B" --title "My title" --x-label "My x label" --y-label "My y label" --hue "column C" --palette "Set2" --style "column D" --markers true --dashes true --ci false --grid true --legend true  
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--hue` is optional, by default it is set to None.
> `--palette` is optional, by default it is set to seaborn's default 'tab10'.
> `--style` is optional, by default it is set to None.
> `--markers` is optional, by default it is set to False.
> `--dashes` is optional, by default it is set to False.
> `--ci` is optional, by default it is set to True.
> `--grid` is optional, by default it is set to True.
> `--legend` is optional, by default it is set to True.
> `--title`, `--x-label` and `--y-label` are optional, by default they are the default values selected by seaborn.
