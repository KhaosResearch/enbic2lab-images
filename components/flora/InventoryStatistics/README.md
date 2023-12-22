# Inventory Statistics

## Overview

This Python script reads an input CSV file containing data and calculates the mean values for specific columns. It then saves the results in a new CSV file. The script is designed to work with CSV files that have the following structure:

- The first row is not the header.
- The first column contains labels for each row.

Here is an example of the input CSV file structure:

```csv
No. of register;NR1;NR2;NR3;NR4
Date;DD-MM-YYYY;DD-MM-YYYY;DD-MM-YYYY;DD-MM-YYYY
Author;A1;A2;A3;A4
Location;L1;L2;L3;L4
UTM;U1;U2;U3;U4
Lithology;Li1;Li2;Li3;Li4
Coverage(%);0;0;0;0
Altitude(m);0;0;0;0
Plot slope;0;0;0;0
Alt. Veg. (cm);0;0;0;0
Plot area(m2);0;0;0;0
Plot orientation;0;0;0;0
Ecology;E1;E2;E3;E4;E5
Community;C1;C2;C3;C4;C5
Species;;;;;
Sp1;-;-;-;-;-
Sp2;-;-;-;-;-
Sp3;-;-;-;-;-
...
Total_Species;0;0;0;0
```

The script calculates the mean values for the "Plot slope," "Alt. Veg. (cm)," and "Plot orientation" columns and saves them in a new CSV file (`output.csv`).

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
docker build -t $REGISTRY/enbic2lab/flora/inventory_statistics:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/inventory_statistics:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/inventory_statistics:1.0.1 --filepath "/mnt/shared/previous_calculations.csv" --delimiter ";"
```
