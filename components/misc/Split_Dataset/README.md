# Split Dataset

## Overview

This script is a generic dataframe processer that receives a CSV file with tabular data and returns another CSV with the data contained in columns `attribute-list`. It could receive a dataset like the following:

| A | B | C | D |
|---|---|---|---|
| 1 | 4 | 3 | 6 |
| 4 | 8 | 5 | 2 |
| 9 | 0 | 3 | 7 |

And you may filter by the columns `A` and `D`. With the `delimiter` ",". So the resulted output would be:

```csv
A,D
1,6
4,2
9,7
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
docker build -t $REGISTRY/enbic2lab/misc/split_dataset:1.0.1 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/split_dataset:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/split_dataset:1.0.1 --filepath "/mnt/shared/inputData.csv" --delimiter ";" --attribute-list "columnA, columnB, columnC"
```
> Output file path may be changed using the `--output-path` argument.