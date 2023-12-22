# Community Statistics

## Overview

The script processes a CSV file containing community data and performs two main tasks: calculating community statistics (`output_comm_statistics.csv`) and generating a species community report (`output_species_comm.csv`). It's designed to work with specific input data columns, the input CSV file should have the following columns:

- `No. of register`: Row index.
- `Date`: Date of the observation.
- `Authors`: Authors of the observation.
- `Group`: Group name (e.g., Flora).
- `Project`: Project name.
- `Community`: Community name (e.g., Pino pinastri-Quercetum cocciferae).
- `Community Authors`: Authors associated with the community.
- `Community Year`: Year of the community observation.
- `Subcommunity`: Subcommunity name.
- `Subcommunity Authors`: Authors associated with the subcommunity.
- `Subcommunity Year`: Year of the subcommunity observation.
- `Location`: Location description.
- `UTM`: UTM coordinates.
- `Natural Park`: Name of the natural park.
- `Lithology`: Lithological information.
- `Coverage(%)`: Percentage of coverage.
- `Altitude(m)`: Altitude in meters.
- `Plot slope`: Slope of the plot.
- `Alt. Veg. (cm)`: Altitude of vegetation in centimeters.
- `Plot area(m2)`: Plot area in square meters.
- `Plot orientation`: Plot orientation.
- `Ecology`: Ecology information.
- `Pictures`: Picture information.
- `Number of Species`: Total number of species.
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
docker build -t $REGISTRY/enbic2lab/flora/community_statistics:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/community_statistics:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/community_statistics:1.0.1 --filepath "/mnt/shared/inventory_transformation.csv" --delimiter ";"
```