# Fidelity Plot

## Overview

The script takes as input a CSV file containing data, parses it, and extracts relevant information. It then generates a network graph using the pyvis library, where nodes represent items from the data, and edges represent relationships between them. The network graph is customized with various options for visualization, such as node size, edge style, and physics simulation parameters. The script also removes nodes that have no connections to improve visualization and displays the resulting interactive network graph as an HTML file.

This script expects a CSV file with the following columns:

- `Index`: Row index.
- `Support`: Relative frequency.
- `Itemsets`: Species.

e.g.:

```csv
;support;itemsets
0;0.25;Species_A,Species_B
1;0.45;Species_B,Species_C
2;0.30;Species_C,Species_D
```

And returns a plot (`output.html`) with the interactive network graph.

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
docker build -t $REGISTRY/enbic2lab/flora/fidelity_plot:1.0.1 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/fidelity_plot:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/fidelity_plot:1.0.1 --filepath "/mnt/shared/support.csv" --delimiter ";"
```
