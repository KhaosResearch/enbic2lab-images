# Word2JSON

## Overview

This script is responsible for processing a Word file and transforming it into a JSON composed of flora inventories. The input word structure is:

```
Athamantetum vayredanae
Persona 1 & Persona 2 in Persona 3, Persona 4 & Persona 5
1982 nom. mut. propos.
var. de Centaurea clementei

INVENTARIO Nº	23	192	205	281
Orientación	N	W	E	W
Inclinación (º)	90	90	90	90
Altitud (m)	1100	1680	1100	1100
Cobertura (%)	10	15	20	5
Área (m 2)	50	3	25	10
Litología	Mármol	Caliza	Dolomía	Dolomía
Altura vegetación (cm)	18	20	15	15

Características de asociación y variante
Athamanta vayredana	1	1	2	1

Diferencial de variante
Centaurea clementei	.	.	1	.

Características de unidades superiores
Campanula mollis	+	+	.	+
Silene andryalifolia	.	.	+	.
Sedum dasyphyllum	.	.	.	+

Compañeras
Chaenorrhinum villosum	.	+	+	+
Rhamnus myrtifolius	.	.	+	1
Teucrium similatum	+	+	.	.
Cephalaria leucantha	.	+	.	.
Helictotrichon filifolium subsp. arundanum	.	+	.	.
Thrincia sp.	.	+	.	.
Sanguisorba minor	.	.	.	+
Scabiosa turolensis subsp. grosii	.	+	.	.

Localidad
23, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.
192, MA: P.N. Sª de las Nieves. Tolox. Cerro Alcazaba. MGRS: UF 2061.
205, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.
281, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.
```

After which it returns a JSON file (`output.json`) with inventories that follow the following structure:

```json
{
    "_id": None,
    "Date": None,
    "Authors": [],
    "Group": "Flora",
    "Project": None,
    "Community": None,
    "Community_Authors": [],
    "Community_Year": None,
    "Subcommunity": None,
    "Subcommunity_Authors": [],
    "Subcommunity_Year": None,
    "Location": None,
    "MGRS": None,
    "Natural_Site": None,
    "Lithology": None,
    "Coverage": None,
    "Altitude": None,
    "Plot_Slope": None,
    "Alt_Veg": None,
    "Plot_Area": None,
    "Plot_Orientation": None,
    "Ecology": None,
    "Species": [],
    "Pictures": [],
    "DataOrigin": "WORD"
}
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
docker build -t $REGISTRY/enbic2lab/flora/word2json:1.0.2 .
```

### Run

Run the image with (assuming that the CSV file is in the `data` folder from the current directory):

```sh
docker run --rm $REGISTRY/enbic2lab/flora/word2json:1.0.2 --help
```

e.g.

```sh
docker run --rm -v $(pwd)/data:/mnt/shared/ $REGISTRY/enbic2lab/flora/word2json:1.0.1 --filepath "/mnt/shared/Tabla_de_prueba.docx" --natural-site "S Nieves"
```
