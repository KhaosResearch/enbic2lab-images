# Fidelity Grade Network Graph Generator

## Overview

This Python script generates an interactive network graph from a CSV file containing species and their connections. The graph shows how different species are connected up to a specified degree. The result is presented in an interactive HTML file and a CSV for future imports.

## Requirements

- Python 3.x
- pandas
- pyvis
- re

## Installation

1. Clone this repository or download the source code.
2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the script, you will need a CSV file with the following format:

```csv
No. of register (ID),test1,test2
Date,,
Authors,,
Group,x,x
Project,,
Community,x,x
Community Authors,"x","x"
Community Year,x,x
Subcommunity,,
Subcommunity Authors,,
Subcommunity Year,,
Location,x,x
MGRS,x,x
Latitude,x,x
Longitude,x,x
Natural Site,x,x
Lithology,,
Coverage(%),x,x
Altitude(m),x,x
Plot slope,x,x
Alt. Veg. (cm),x,x
Plot area(m2),x,x
Plot orientation,x,x
Ecology,,
Pictures,,
Number of Species,x,x
Species,,
Species1,-,-
Species2,-,-
Species3,-,-
Species4,-,-
```

Run the script with the following command:

```sh
python main.py --filepath "path/to/your/file.csv" --species "Species_A" --grade 2
```

This will generate a network graph for `Species_A` up to grade 2.

## Output

The script produces two files:

- `output.html`: An interactive network graph.
- `output.csv`: Graph data that can be imported into tools like Gephi or Neo4j.

## Tests

To run unit tests, install the necessary dependencies and execute the test script:

```sh
pip install -r requirements-dev.txt
python -m pytest
```

## Docker Support

### Building the Docker Image

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/flora/fidelity-grade:1.0.1 .
```

### Running the Docker Container

Run the container with:

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/fidelity-grade:1.0.1 --filepath "/mnt/shared/ETP_Hargreaves_complete.csv" --species "Lavandula lanata" --grade 2
```

## Contributing

If you wish to contribute to this project, feel free to fork and send your pull requests.

## License

[MIT License](LICENSE)

