# XLSX2CSV

## Overview

Join two csv datasets using columns as keys

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
python -m pytest
```

## Docker

### Build

Build the image with:

```sh
docker build -t enbic2lab/misc/join_dataset:1.0.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm enbic2lab/misc/join_dataset:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ enbic2lab/misc/join_dataset:1.0.0 --first-file-path "/mnt/shared/ETP_preprocessing.csv" --index-column-first-file "Fecha" --second-file-path "/mnt/shared/precipitation_data.csv" --index-column-second-file "Fecha" --delimiter-file-1 ";" --delimiter-file-2 ";" --delimiter ";" --join-how-parameter "left"
```
