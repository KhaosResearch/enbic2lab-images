# Sum Species Statistics Plot

## Overview

This script takes care of plot the top n species of the species_statistics CSV File. It's designed to work with specific input data columns, the input CSV file should have the following columns:

- `Species`: This column contains the names of botanical species. Each row represents a different species. Some examples of species names in this column include "Lavandula stoechas L.," "Arenaria montana L. subsp. intricata (Ser.) Pau," etc.

- `Sum_Species`: This column contains integer numbers representing the sum of species.

- `Coverage_mean_percentage`: This column seems to contain percentage range data in text format. These percentage ranges may represent information related to the average coverage of the species. However, it's important to note that they are in text format, not numeric format. Some examples of values in this column include "2-5," "1-2," etc.

Upon execution, the component generates a bar chart (`output.pdf`)

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
docker build -t $REGISTRY/enbic2lab/flora/sum_species_statistics_plot:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/sum_species_statistics_plot:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/sum_species_statistics_plot:1.0.1 --filepath "/mnt/shared/species_statistics.csv" --delimiter ";" --n-samples 20 --color-plot "#006400"
```
