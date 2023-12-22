# Joint Plot

## Overview
This component creates a generic joint plot from any csv file indicating the columns to be plotted and some customizable parameters.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_jointplot:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_jointplot:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_jointplot:1.0.0 --filepath /mnt/shared/input.csv --delimiter ";" --x-column "column A" --y-column "column B" --color "red" --title "My title" --x-label "My x label" --y-label "My y label"
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--color` is optional, by default it uses the seaborn's default color.
> `--title`, `--x-label` and `--y-label` are optional, by default they are the default values selected by seaborn.
