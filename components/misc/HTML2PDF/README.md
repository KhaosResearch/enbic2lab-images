# HTML TO PDF

## Overview

This component receives any kind of HTML file and converts it to PDF using wkhtmltopdf library.

## Usage
Create a virtual environment and install the requirements, including wkhtmltopdf:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
sudo apt-get install -y wkhtmltopdf
```

Then run the script with:
```sh
python main.py --help
```

## Test
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
docker build -t $REGISTRY/enbic2lab/misc/html2pdf:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/misc/html2pdf:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/html2pdf:1.0.0 --filepath /mnt/shared/input.html
```
> The output path may be changed using the `--output-path` argument.