# JSON2DB

## Overview

## Usage

Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then, run the script with:

```sh
source .env 
python main.py --help
```

## Docker

### Build

Build the image with:

```sh
source .env
docker build -t $REGISTRY/enbic2lab/flora/json2db:1.0.0 \
            --build-arg mongo_host=${MONGO_HOST} \
            --build-arg mongo_username=${MONGO_USERNAME} \
            --build-arg mongo_access_key=${MONGO_ACCESS_KEY} \
            --build-arg mongo_database=${MONGO_DATABASE} .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/json2db:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/json2db:1.0.0 --filepath /mnt/shared/sample.json --collection-name floras_samples --collision_policy ignore
```