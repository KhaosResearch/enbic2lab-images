# Community Statistics Plot

## Overview

This script expects a CSV file with the following columns:

- `Community`: Community name.
- `Min_Alt`: Minimum altitude of the community.
- `Max_Alt`: Maximum altitude of the community.

e.g.:

```csv
Community;Min_Alt;Max_Alt
Community A;100;200
Community B;150;250
Community C;200;300
```

And returns a plot (`output.pdf`) with the altitude range per community.

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
docker build -t $REGISTRY/enbic2lab/flora/community_statistics_plot:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/community_statistics_plot:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/community_statistics_plot:1.0.1 --filepath "/mnt/shared/community_altitude_range.csv" --delimiter ";"
```