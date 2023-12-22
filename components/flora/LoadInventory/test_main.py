import json
import unittest

import pandas as pd

from main import generate_df, main


class MockCollection:
    def __init__(self, data):
        self.data = data

    def find(self, query):
        return [item for item in self.data if self._matches_query(item, query)]

    def count_documents(self, query):
        return len(self.find(query))

    def _matches_query(self, item, query):
        for key, value in query.items():
            if key not in item or item[key] != value:
                return False
        return True


def test_conect_to_DB2(mocker):
    with open("test_collection.json", "r") as file:
        data = json.load(file)
    collection = MockCollection(data)
    mocker.patch("main.connect_to_DB", return_value=collection)
    mocker.patch("main.check_presence", return_value="")
    mocker.patch("main.check_presence_for_list", return_value="")
    result = main(
        start_date="",
        end_date="",
        community_start_year="",
        community_end_year="",
        subcommunity_start_year="",
        subcommunity_end_year="",
        project="",
        natural_site="Sierra de las Nieves",
        altitude="",
        lithology="",
        plot_orientation="",
        plot_slope="",
        phyto_index="",
        num_species="",
        community="",
        location="",
        author="",
        community_author="",
        subcommunity_author="",
        species="",
        output="mnt/shared/test_output.csv",
    )
    # Result does not return anything
    assert result is None


def test_generate_df(mocker):
    # Create a mock object for the function transform_to_dataframe
    mock_transform = mocker.patch("main.transform_to_dataframe")

    attributes = {
        "No. of register (ID)": "S-P25532",
        "Date": None,
        "Authors": "",
        "Group": "Flora",
        "Project": None,
        "Community": "Rhamno pumili-Saxifragetum granatensis",
        "Community Authors": "Pérez Latorre,Cabezudo",
        "Community Year": 1998,
        "Subcommunity": "galietosum pulvinati",
        "Subcommunity Authors": "Pérez Latorre,Cabezudo",
        "Subcommunity Year": 1999,
        "Location": "Malaga. P.N. S. de las Nieves. Tolox. Cerro Plazoleta. por detras del pilar de Tolox",
        "MGRS": "30SUF2161",
        "Latitude": 36.682396874521615,
        "Longitude": -4.997761664922841,
        "Natural Site": "Sierra de las Nieves",
        "Lithology": None,
        "Coverage(%)": 100,
        "Altitude(m)": 1720,
        "Plot slope": 10,
        "Alt. Veg. (cm)": 4,
        "Plot area(m2)": 300,
        "Plot orientation": "NE",
        "Ecology": None,
        "Pictures": "",
        "Number of Species": 23,
        "Species": "",
    }
    species = {"Abies pinsapo": "+"}
    mock_transform.return_value = (attributes, species)

    definitive_list = [
        {
            "_id": "S-P25532",
            "Alt_Veg": 4,
            "Altitude": 1720,
            "Authors": [],
            "Community": "Rhamno pumili-Saxifragetum granatensis",
            "Community_Authors": ["Pérez Latorre", "Cabezudo"],
            "Community_Year": 1998,
            "Coverage": 100,
            "Date": None,
            "Ecology": None,
            "Group": "Flora",
            "Latitude": 36.682396874521615,
            "Lithology": None,
            "Location": "Malaga. P.N. S. de las Nieves. Tolox. Cerro Plazoleta. por detras del pilar de Tolox",
            "Longitude": -4.997761664922841,
            "Natural_Site": "Sierra de las Nieves",
            "Pictures": [],
            "Plot_Area": 300,
            "Plot_Orientation": "NE",
            "Plot_Slope": 10,
            "Project": None,
            "Species": [
                {"Name": "Abies pinsapo", "Ind": "+"},
                {"Name": "Armeria villosa", "Ind": "+"},
                {"Name": "Achillea odorata", "Ind": "+"},
                {"Name": "Daphne laureola", "Ind": "2"},
                {"Name": "Helleborus foetidus", "Ind": "+"},
                {"Name": "Quercus faginea", "Ind": "1"},
                {"Name": "Acer monspessulanum", "Ind": "+"},
                {"Name": "Crataegus monogyna", "Ind": "4"},
                {"Name": "Hyacinthoides hispanica", "Ind": "+"},
                {"Name": "Ulex baeticus subsp. baeticus", "Ind": "+"},
                {"Name": "Prunus spinosa", "Ind": "+"},
                {"Name": "Helichrysum stoechas", "Ind": "+"},
                {"Name": "Cerastium gibraltaricum", "Ind": "+"},
                {"Name": "Viscum cruciatum", "Ind": "1"},
                {"Name": "Aristolochia paucinervis", "Ind": "+"},
                {"Name": "Tamus communis", "Ind": "+"},
                {"Name": "Lotus edulis", "Ind": "+"},
                {"Name": "Geranium molle", "Ind": "1"},
                {"Name": "Scrophularia scorodonia", "Ind": "+"},
                {"Name": "Silene vulgaris subsp. vulgaris", "Ind": "+"},
                {"Name": "Paeonia coriacea", "Ind": "2"},
                {"Name": "Quercus rotundifolia", "Ind": "+"},
                {"Name": "Sorbus aria", "Ind": "+"},
            ],
            "Subcommunity": "galietosum pulvinati",
            "Subcommunity_Authors": ["Pérez Latorre", "Cabezudo"],
            "Subcommunity_Year": 1999,
            "MGRS": "30SUF2161",
            "dataOrigin": "SIVIM",
        }
    ]
    result = generate_df(definitive_list)

    # Verify that transform_to_dataframe was called with the correct arguments
    mock_transform.assert_called_with(definitive_list[0])

    attributes.update(species)
    df = pd.DataFrame(attributes.items(), columns=["Attributes", "Values"]).set_index(
        "Attributes"
    )

    col_dict = dict.fromkeys(df.columns, "")

    df.rename(columns=col_dict, inplace=True)
    df.index.name = None

    result.to_csv(index_label="No. of register (ID)") == df.to_csv(
        header=None, index=True
    )


if __name__ == "__main__":
    unittest.main()
