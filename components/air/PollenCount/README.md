# Pollen Count

## Overview

This script counts the number of pollen grains in a bunch of TIFF images given inside a ZIP file. It then returns the results as a CSV file and a JSON file. These files also include information about the date and name of the experiment.

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

## Docker

### Build

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/air/pollen_count:1.0.2 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/air/pollen_count:1.0.2 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/pollencount:1.0.2 --filepath "/mnt/shared/imagesZipped.zip" --delimiter ";" --sample-name "Experiment 1" --sample-date "2021-01-01"
```
> Output path may be changed using `--output-path`. By default, it is `/mnt/shared/`.
> `--sample-name` is compulsory but it may be an empty string. `--sample-date` is optional.
> `--delimiter` is optional and defaults to `,`.