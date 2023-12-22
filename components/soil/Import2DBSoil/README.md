# Import to DB

## Overview

Create JSON file from Excel file, unzip the images corresponding to the data, upload these images to Minio and upload the JSON file to MongoDB

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
source .env
docker build -t $REGISTRY/enbic2lab/flora/import2db_soil:1.0.1 \
            --build-arg mongo_host=${MONGO_HOST} \
            --build-arg mongo_username=${MONGO_USERNAME} \
            --build-arg mongo_access_key=${MONGO_ACCESS_KEY} \
            --build-arg mongo_database=${MONGO_DATABASE} \
            --build-arg mongo_collection=${MONGO_COLLECTION} \
            --build-arg minio_endpoint=${MINIO_ENDPOINT} \
            --build-arg minio_access_key=${MINIO_ACCESS_KEY} \
            --build-arg minio_secret_key=${MINIO_SECRET_KEY} .
```


### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/import2db_soil:1.0.1 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/import2db_soil:1.0.1  --filepath "/mnt/shared/parques_naturales.xlsx" --compressed-file "/mnt/shared/lifewatch-prueba.zip" --compressed-file2 "/mnt/shared/Espectro.zip" 

```
