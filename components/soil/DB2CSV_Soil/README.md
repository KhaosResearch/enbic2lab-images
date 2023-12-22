# DB to CSV (soil)

## Overview
This script uses a MongoDB database to retrieve information about certain soil parcel. It uses several parameters to filter the MongoDB query that will be used to get the information.

The information retrieved will be returned as a CSV file with the following fields:
- Aggregate_Stability
- Altitude
- Apparent_Density
- Author
- C_Factor
- Clays
- Coarse_Sands
- Coarse_Silts
- Date
- Electric_Conductivity
- Env_photo_path
- Field_Capacity
- Fine_Sands
- Fine_Silts
- Gravels
- Group
- Hydrophobicity
- Incidence
- K_Factor
- Latitude
- Lithology
- Longitude
- Medium_Sands
- Natural_Site
- Organic_Carbon
- Organic_Matter
- Orientation
- Permanent_Wilting_Point
- Permeability
- Project
- SSC_1
- SSC_Photo_Path
- Slope
- Spectral_Response_Path
- Texture_Class
- Texture_Class_Julian
- Total_Sands
- Total_Silts
- Useful_Water
- Uses2
- Uses3
- Very_Coarse_Sands
- Very_Fine_Sands
- pH

> Component done by:
> - Daniel Doblas Jiménez (dandobjim@uma.es),
> - Irene SÃ¡nchez Jiménez (iresanjim@uma.es),
> - María Luisa Antequera (marialan@uma.es)
> - Irene Romero Granados (ireero99@gmail.com)
> - Juan Sánchez Rodríguez (juansanchezrodriguez1999@uma.es)
> - Juan Carlos Ruiz Ruiz (juancaruru@uma.es)

## Usage
There are 3 options to configure the database data:
  1. Copy the `.env.template` file and rename it as `.env`. Then fill it up with your own MongoDB information.
  2. Change the `Dockerfile` and add the database information as environment variables.
  3. Use the docker image and pass the database information as environment variables. Using `-e` and giving the variables `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD` and `MONGO_DB`.

Then continue with the usual procedure. Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
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
python -m unittest discover .
```
## Docker

### Build
Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/soil/db2csv_soil:1.1.4 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/soil/db2csv_soil:1.1.4 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/soil/db2csv_soil:1.1.4
```
> The output file path may be changed using the `--output-path` parameter.

> **Note**: If no parameter is inserted the component will return all the database data and will return int in a CSV with semicolons as separators. The possible parameters are:
> - `--id`: Identificator number of an especific sample
> - `--author`: List of authors of the sample
> - `--description`: Description of the sample
> - `--natural-site-list`: List of natural sites of the sample
> - `--project`: Project name of the sample
> - `--start-date`: Starting date for search samples by date range
> - `--end-date`: End date for search samples by date range
> - `--delimiter`: Delimiter to use when saving the CSV file

