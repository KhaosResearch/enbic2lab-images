# ImportFile

## Overview

The script downloads a file from a given URL.

Valid schemes are:
* `http://`
* `https://`
* `minio://`

> Warning:
> 
> This component is designed to download files from any specified URL. Due to its generic nature, the output format can't be predetermined. Therefore, there exists multiple versions of this component, each one tailored to a specific use case.

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

Run the tests with:

```sh
python test_main.py
```

## Docker

### Build

Set the required environment variables in the `Dockerfile`.

Then, build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/misc/importfile:1.1.0 .
```

### Run

Run the image with (assuming that the file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/misc/importfile:1.1.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/misc/importfile:1.1.0 --url "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
```
