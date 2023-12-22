# Mean Coverage Barplot

## Overview
The script takes care of plot the Mean Coverage per community from a CSV File. It's designed to work with specific input data columns, the input CSV file should have the following columns:

- `Community`: This field represents the name of the ecological community or vegetation type in the specific area that the CSV row refers to.
- `Mean Coverage`: Indicates the average percentage of vegetation cover for the specified community.
- `Mean Coverage Standard Error`: It is the standard error of the average of the percentage of vegetation cover.
- `Altitude Difference`: Represents the difference in altitude for the community in meters.
- `Min_Alt`: It is the minimum altitude value in meters for the community.
- `Max_Alt`: Indicates the maximum altitude value in meters for the community.
- `Number of Species`: Shows the number of plant species present in the specific ecological community.

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
docker build -t $REGISTRY/enbic2lab/flora/mean_coverage_barplot:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/mean_coverage_barplot:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/mean_coverage_barplot:1.0.1 --filepath "/mnt/shared/community_statistics.csv" --delimiter ";"
```