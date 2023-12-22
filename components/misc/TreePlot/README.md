# Tree plot

## Overview
This component creates a generic Tree plot from any csv file indicating the column to be analyzed and some more styling options.

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
docker build -t $REGISTRY/enbic2lab/misc/generic_treeplot:1.0.2 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/generic_treeplot:1.0.2 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/generic_treeplot:1.0.2 --filepath /mnt/shared/input.csv --delimiter ";" --target-col "column A" --label "column B" --palette "Set1" --title "My title"
```
> The output file path may be changed using the `--output-path` argument.
> `--delimiter` is optional, by default it is set to ",".
> `--label` is optional, by default it is set to None. **`--label` column must have the same frequency as `--target-col`**
> `--palette` may receive a palette name or a list of colors. Ir is optional, if non present or wrong input it is set to default: "viridis".
> `--title` is optional, by default it is set to None.