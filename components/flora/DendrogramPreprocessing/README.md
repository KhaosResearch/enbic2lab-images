## Preprocessing

## Overview

The purpose of this code is to transform the flora csv into a DataSet useful for the creation of the dendrogram. To do this: elimination of unnecessary initial columns up to species and reduce headers and curate values ("+"=0.2, "-"=0, "(+)"=0.1, "+.2"=0.2, "X"=0, "."=0). It's designed to work with specific input data columns, the input CSV file should have the following columns:

- `No. of register`: Row index.
- `Date`: Date of the observation.
- `Author`: Author of the observation.
- `Location`: Location description.
- `UTM`: UTM coordinates.
- `Lithology`: Lithological information.
- `Coverage(%)`: Percentage of coverage.
- `Altitude(m)`: Altitude in meters.
- `Plot slope`: Slope of the plot.
- `Alt. Veg. (cm)`: Altitude of vegetation in centimeters.
- `Plot area(m2)`: Plot area in square meters.
- `Plot orientation`: Plot orientation.
- `Ecology`: Ecology information.
- `Community`: Community name (e.g., Pino pinastri-Quercetum cocciferae).
- `Species`: Species names.

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
docker build -t $REGISTRY/enbic2lab/flora/preprocessing:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/preprocessing:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/preprocessing:1.0.1 --filepath "/mnt/shared/inventories.csv" --delimiter ";"
```


