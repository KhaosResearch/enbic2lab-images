import copy
import unittest

from docx import Document

from main import INVENTORY_TEMPLATE, extract_data, fill_json, ind_transform

INPUT_DOC = [
    "Athamantetum vayredanae",
    "Persona 1 & Persona 2 in Persona 3, Persona 4 & Persona 5",
    "1982 nom. mut. propos.",
    "var. de Centaurea clementei",
    "",
    "INVENTARIO Nº\t23\t192\t205\t281",
    "Orientación\tN\tW\tE\tW",
    "Inclinación (º)\t90\t90\t90\t90",
    "Altitud (m)\t1100\t1680\t1100\t1100",
    "Cobertura (%)\t10\t15\t20\t5",
    "Área (m 2)\t50\t3\t25\t10",
    "Litología\tMármol\tCaliza\tDolomía\tDolomía",
    "Altura vegetación (cm)\t18\t20\t15\t15",
    "",
    "Características de asociación y variante",
    "Athamanta vayredana\t1\t1\t2\t1",
    "",
    "Diferencial de variante",
    "Centaurea clementei\t.\t.\t1\t.",
    "",
    "Características de unidades superiores",
    "Campanula mollis\t+\t+\t.\t+",
    "Silene andryalifolia\t.\t.\t+\t.",
    "Sedum dasyphyllum\t.\t.\t.\t+",
    "",
    "Compañeras",
    "Chaenorrhinum villosum\t.\t+\t+\t+",
    "Rhamnus myrtifolius\t.\t.\t+\t1",
    "Teucrium similatum\t+\t+\t.\t.",
    "Cephalaria leucantha\t.\t+\t.\t.",
    "Helictotrichon filifolium subsp. arundanum\t.\t+\t.\t.",
    "Thrincia sp.\t.\t+\t.\t.",
    "Sanguisorba minor\t.\t.\t.\t+",
    "Scabiosa turolensis subsp. grosii\t.\t+\t.\t.",
    "",
    "Localidad",
    "23, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.",
    "192, MA: P.N. Sª de las Nieves. Tolox. Cerro Alcazaba. MGRS: UF 2061.",
    "205, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.",
    "281, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960.",
]

INITIAL_LIST = [
    ["Athamantetum vayredanae"],
    ["Persona 1 & Persona 2 in Persona 3, Persona 4 & Persona 5"],
    ["1982 nom. mut. propos."],
]

ARGUMENT_LIST = [
    ["INVENTARIO Nº", "23", "192", "205", "281"],
    ["Orientación", "N", "W", "E", "W"],
    ["Inclinación (º)", "90", "90", "90", "90"],
    ["Altitud (m)", "1100", "1680", "1100", "1100"],
    ["Cobertura (%)", "10", "15", "20", "5"],
    ["Área (m 2)", "50", "3", "25", "10"],
    ["Litología", "Mármol", "Caliza", "Dolomía", "Dolomía"],
    ["Altura vegetación (cm)", "18", "20", "15", "15"],
]

SPECIES_LIST = [
    ["Athamanta vayredana", "1", "1", "2", "1"],
    ["Centaurea clementei", ".", ".", "1", "."],
    ["Campanula mollis", "+", "+", ".", "+"],
    ["Silene andryalifolia", ".", ".", "+", "."],
    ["Sedum dasyphyllum", ".", ".", ".", "+"],
    ["Chaenorrhinum villosum", ".", "+", "+", "+"],
    ["Rhamnus myrtifolius", ".", ".", "+", "1"],
    ["Teucrium similatum", "+", "+", ".", "."],
    ["Cephalaria leucantha", ".", "+", ".", "."],
    ["Helictotrichon filifolium subsp. arundanum", ".", "+", ".", "."],
    ["Thrincia sp.", ".", "+", ".", "."],
    ["Sanguisorba minor", ".", ".", ".", "+"],
    ["Scabiosa turolensis subsp. grosii", ".", "+", ".", "."],
]

LOCALITY_LIST = [
    [
        "23, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960."
    ],
    ["192, MA: P.N. Sª de las Nieves. Tolox. Cerro Alcazaba. MGRS: UF 2061."],
    [
        "205, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960."
    ],
    [
        "281, MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas. MGRS: UF 1960."
    ],
]

NUM_INVENTARIOS = 4


class TestExtractData(unittest.TestCase):
    def test_extract_data(self):
        # Simula un documento de entrada
        doc = Document()
        for paragraph in INPUT_DOC:
            doc.add_paragraph(paragraph)

        # Llama a la función para extraer los datos
        (
            initial_list,
            argument_list,
            species_list,
            locality_list,
            num_inventarios,
        ) = extract_data(doc)

        # Realiza las aserciones para comprobar si la función produce los resultados esperados
        self.assertEqual(
            initial_list,
            INITIAL_LIST,
        )
        self.assertEqual(
            argument_list,
            ARGUMENT_LIST,
        )
        self.assertEqual(
            species_list,
            SPECIES_LIST,
        )
        self.assertEqual(
            locality_list,
            LOCALITY_LIST,
        )
        self.assertEqual(num_inventarios, NUM_INVENTARIOS)

    def test_ind_transform(self):
        assert ind_transform("(+)") == "+"
        assert ind_transform("+.2") == "+"
        assert ind_transform(".") == "-"
        assert ind_transform("x") == "-"
        assert ind_transform("X") == "-"
        assert ind_transform("r") == "+"
        assert ind_transform("abc") == "a"
        assert ind_transform("123") == "1"

    def test_fill_json(self):
        # Llama a la función para llenar el JSON
        filled_json_set = fill_json(
            [copy.deepcopy(INVENTORY_TEMPLATE) for _ in range(NUM_INVENTARIOS)],
            "Test Site",
            INITIAL_LIST,
            ARGUMENT_LIST,
            SPECIES_LIST,
            LOCALITY_LIST,
            NUM_INVENTARIOS,
        )

        # Realiza las aserciones para comprobar si la función produce los resultados esperados
        self.assertEqual(filled_json_set[0]["_id"], "23-Athamantetum_vayredanae")
        self.assertEqual(filled_json_set[0]["Community"], "Athamantetum vayredanae")
        self.assertEqual(filled_json_set[0]["Community_Year"], 1982)
        self.assertEqual(
            filled_json_set[0]["Authors"],
            ["Persona 3", "Persona 4", "Persona 5"],
        )
        self.assertEqual(
            filled_json_set[0]["Location"],
            "MA: P.N. Sª de las Nieves. Tolox. Carril base del Torrecillas.",
        )
        self.assertEqual(filled_json_set[0]["MGRS"], "30SUF1960")
        self.assertEqual(filled_json_set[0]["Altitude"], "1100")
        self.assertEqual(filled_json_set[0]["Plot_Orientation"], "N")
        self.assertEqual(filled_json_set[0]["Plot_Slope"], "90")
        self.assertEqual(filled_json_set[0]["Coverage"], "10")
        self.assertEqual(filled_json_set[0]["Plot_Area"], "50")
        self.assertEqual(filled_json_set[0]["Lithology"], "Mármol")
        self.assertEqual(filled_json_set[0]["Alt_Veg"], "18")
        self.assertEqual(len(filled_json_set[0]["Species"]), 13)
        self.assertEqual(filled_json_set[0]["DataOrigin"], "WORD")


if __name__ == "__main__":
    unittest.main()
