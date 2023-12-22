# Image Extract

## Overview
This component extracts images from a ZIP file of a given format and saves them in a folder. It is compulsory to have java installed in the system and the java executable mentioned below. It is also necessary to have `python-dev` installed so that the `python-javabridge` package can be installed.

It is highly recommended to use docker for the execution of this component.

## Usage
Install Java JDK 11 and set the `JAVA_HOME` environment variable to the path of the JDK installation. For example:

```sh
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

Download the `bioformats_package.jar` file from [here](https://downloads.openmicroscopy.org/bio-formats/6.5.1/artifacts/bioformats_package.jar) and place it in the `bioformats` folder.

```sh
curl -o ./bioformats/bioformats_package.jar https://downloads.openmicroscopy.org/bio-formats/6.9.1/artifacts/bioformats_package.jar
```

Create a virtual environment and install the requirements:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If this fails with an error related to `python-javabridge`, install `python-dev` and try again.

```sh
sudo apt-get install python-dev
```

Then run the script with:
```sh
python main.py --help
```

## Docker

### Build
Build the image with:

```sh
docker build -t $REGISTRY/enbic2lab/air/image_extract:1.0.0 .
```

### Run
Run the image with:

```sh
docker run --rm $REGISTRY/enbic2lab/air/image_extract:1.0.0 --help
```

e.g.
```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/air/image_extract:1.0.0 --filepath /mnt/shared/sampleImages.zip --file-extension vsi --image-name-regex "" --min-image-size 10000
```
> `--file-extension` is optional, if not provided, 'vsi' is used as default value. You must use only the extension, without the dot.
> `--image-name-regex` is optional, if not provided, all images are extracted. You can use a regex to extract only the images that match the regex.
> `--min-image-size` is optional, if not provided, all images are extracted. You may insert the size in pixels.
> `--output-path` is optional, `/mnt/shared/` will be used by default. **It is compulsory to write the trailing slash**.
