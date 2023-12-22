# Excel 2 Sample and Taxon JSONs

## Overview
Given an XLSX input with flora sampling data, information is divided into two output JSON files. The first contains the exclusive information of the samples (`sample.json`), and the second, taxonomic information of the species (`taxon.json`). The XLSX input file must have the following columns:

- `ENBIC2ID:` Unique identification for each sample
- `NaturalSite:` Natural site where the sample was collected
- `gbifID:` Unique identification assigned by the Global Biodiversity Information Facility (GBIF) for the record
- `institutionCode:` Code of the institution that collected or maintains the specimen
- `catalogNumber:` Catalog number associated with the specimen
- `kingdom:` Kingdom to which the plant belongs
- `phylum:` Phylum to which the plant belongs
- `order:` Taxonomic order of the plant
- `class:` Taxonomic class of the plant
- `family:` Taxonomic family of the plant
- `genus:` Genus of the plant
- `hib:` Hybridization (boolean)
- `aut_esp`: Author of the species
- `species:` Name of the species
- `taxonRank:` Taxonomic rank of the plant
- `infraspecificEpithet:` Infraspecific epithet
- `aut_infra:` Author of the infraspecific taxon
- `scientificName:` Complete scientific name of the plant
- `taxonRankInterpreted:` Interpreted taxonomic rank
- `speciesInterpreted:` Interpreted name of the species
- `identifiedBy:` Person who identified the plant
- `dateIdentified:` Date when the plant was identified
- `countryCode:` Code of the country where the plant was collected
- `stateProvince:` Province or state where the plant was collected
- `locality:` Specific locality where the plant was collected
- `decimalLatitude:` Geographic latitude in decimal format
- `decimalLongitude:` Geographic longitude in decimal format
- `MGRS:` Military Grid Reference System
- `coordinateUncertaintyInMeters:` Uncertainty in geographical coordinates in meters
- `elevation:` Elevation of the collection site
- `recordedBy:` Person who recorded information about the specimen
- `eventDate:` Date of the collection event
- `remarks:` Additional observations or comments

The first JSON with the exclusive information of the samples (`sample.json`) will be form:

```json
[
    {
    "specieName": "",
    "ENBIC2ID": 1,
    "Natural_Site": "",
    "gbifID": "",
    "institutionCode": "",
    "catalogNumber": "",
    "scientificName": "",
    "aut_infra": "",
    "taxonRankInterpreted": "",
    "speciesInterpreted": "",
    "identifiedBy": "",
    "dateIdentified": "",
    "countryCode": "",
    "stateProvince": "",
    "locality": "",
    "Latitude": ,
    "Longitude": ,
    "coordinateUncertaintyInMeters": "",
    "elevation": "",
    "recordedBy": "",
    "eventDate": "",
    "remarks": "",
    "MGRS": ""
    },
    //...
]
```

And the second JSON with the taxonomic information of the species (`taxon.json`) will be form:

```json
[
    {
    "genus": "",
    "species": "",
    "taxonRank": "",
    "taxonRankAcronym": "",
    "infraspecificEpithet": "",
    "kingdom": "",
    "phylum": "",
    "order": "",
    "class": "",
    "family": "",
    "aut_esp": "",
    "specieName": ""
    },
    //...
]
```


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
docker build -t $REGISTRY/enbic2lab/flora/excel_2_sample_and_taxon_jsons:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/excel_2_sample_and_taxon_jsons:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/excel_2_sample_and_taxon_jsons:1.0.0 --filepath "/mnt/shared/flora_excel.xlsx"
```