# Analyse Trend

## Overview 

This script takes a input CSV file with daily pollen samples and perform a trend analysis. This generates a PDF file (`output.pdf`) and another XLSX (` output.xlsx`). The input CSV format is as follows:

```csv
"date","PollenA","PollenB","PollenC","PollenD"
2010-02-25,0,0,0,0
2010-02-26,0,0,0,0
2010-02-27,0,0,0,0
2010-02-28,0,0,0,0
2010-03-01,0,0,0,0
2010-03-02,0,0,0,0
```

## Usage

Function for the installation of packages specified in requirements.txt

```sh
install_requirements () {
    file=$1
    lib=$2

    # Create the local library folder
    mkdir $lib

    # Install R packages
    Rscript -e "install.packages('remotes', lib='$lib')"

    ## Cran repository
    for line in $(grep "^cran" $file); do \
        pkg=${line#*/}; pkg=${pkg%%==*}; version=${line#*==}; \
        Rscript -e "remotes::install_version('$pkg', version = '$version', dependencies = TRUE, lib='$lib')" || exit 1; \
    done
        
    ## Bioconductor repository
    for line in $(grep "^bioconductor" $file); do \
        pkg=${line#*/}; pkg=${pkg%%==*}; version=${line#*==}; \
        Rscript -e "remotes::install_bioc('$version/$pkg', dependencies = TRUE, lib='$lib')" || exit 1; \
    done
}
export -f install_requirements
```

Download the packages specified in the requirements.txt in a local library folder

```sh
install_requirements "requirements.txt" "rlocallibrary"
```

Then, run the script with:

```sh
Rscript main.R --help
```

## Tests

Install the requirements for testing:

```sh
install_requirements "requirements-dev.txt" "rlocallibrary-dev"
```

Run the tests with:

```sh
Rscript test_main.R rlocallibrary-dev
```

## Docker

### Build

Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/air/analyse_trend:1.0.0 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/air/analyse_trend:1.0.0 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/analyse_trend:1.0.0 --filepath /mnt/shared/munich.csv
```