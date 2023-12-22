import os
from tempfile import TemporaryDirectory

import pytest

from main import indTransform, main, resetJsonDict

sample_XML_file = '''<ReleveTable xmlns="http://biodiver.bio.ub.es/vegana/resources/schemas" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" code="V-P02856+V-P03026+V-P02107+V-P02575++V-P02856" releve_table_xml_version="1.2" thesaurus_id="tesaTAX.xml+tesaTAX.xml" xsi:schemaLocation="http://biodiver.bio.ub.es/vegana/resources/schemas http://biodiver.bio.ub.es/vegana/resources/schemas/ReleveTable1.2.xsd">
<Releve name="V-P03026" type="BB">
<OriginalSource>
<InstitutionCode>SIVIM</InstitutionCode>
<InstitutionName>Sistema de Información de la Vegetación Ibérica y Macaronésica</InstitutionName>
<SourceWebAddress>http://www.sivim.info</SourceWebAddress>
</OriginalSource>
<SurveyDate day="20" hour="0" minutes="0" month="5" seconds="0" year="2098"/>
<PlotArea>200.0</PlotArea>
<PlotForm>0</PlotForm>
<OriginalSyntaxonName>Rusco hypophylli-Quercetum canariensis Rivas Goday &amp; Rivas Mart. ex Rivas Mart. 1974 subass. quercetosum broteroi Pérez Latorre &amp; Cabezudo in Pérez Latorre &amp; al. 1996</OriginalSyntaxonName>
<CurrentSyntaxonName>Rusco hypophylli-Quercetum canariensis Rivas-Martínez 1975</CurrentSyntaxonName>
<BibliographicReference>
<WorkCode>0075</WorkCode>
<WorkName>Red de Información Ambiental de Andalucía (REDIAM)</WorkName>
<WorkAuthors>varios autores</WorkAuthors>
<WorkPublicationYear>2017</WorkPublicationYear>
<WorkPublication>Junta de Andalucía</WorkPublication>
<LocationInWork/>
</BibliographicReference>
<CitationCoordinate code="30STF6762" precision="0.0" type="UTM alphanum" units="1Km"/>
<ReleveEntry layer="2" original_name="Adenocarpus telonensis (Loisel.) DC. in Lam. &amp; DC." value="+"/>
<ReleveEntry layer="2" original_name="Ruscus aculeatus L." value="+"/>
<ReleveEntry accepted_name="Crataegus monogyna Jacq." layer="2" original_name="Crataegus monogyna Jacq. subsp. brevispina (Kunze) Franco" value="+"/>
<ReleveEntry layer="2" original_name="Osyris alba L." value="1"/>
<ReleveEntry layer="3" original_name="Vinca difformis Pourr." value="+"/>
<SideData type="ECO"/>
<SideData type="GEO">
<Datum label="Locality" name="locality">
<value>Andaluc¡a</value>
</Datum>
<Datum label="Altitude" name="altitude">
<value>15</value>
</Datum>
</SideData>
<SideData type="STRUCT">
<Datum label="Herb Cover (%)" name="herb_cover">
<value>95</value>
</Datum>
<Datum label="Total Cover (%)" name="total_cover">
<value>70</value>
</Datum>
</SideData>
<ReleveComments/>
</Releve>
<ReleveTableEntry layer="2" original_name="Adenocarpus telonensis (Loisel.) DC. in Lam. &amp; DC."/>
<ReleveTableEntry layer="3" original_name="Asplenium onopteris L."/>
<ReleveTableEntry layer="2" original_name="Asparagus aphyllus L."/>
<ReleveTableEntry layer="3" original_name="Cynosurus elegans Desf."/>
<ReleveTableEntry layer="2" original_name="Erica arborea L."/>
<ReleveTableEntry layer="2" original_name="Lavandula stoechas L. subsp. stoechas"/>
<ReleveTableEntry layer="2" original_name="Lonicera implexa Aiton"/>
<TableVisualOptions/>
</ReleveTable>
''' 

@pytest.fixture
def sample_xml_file():
    with TemporaryDirectory() as temp_dir:
        temp_csv_file = os.path.join(temp_dir, "input.xml")
        with open(temp_csv_file, "w") as f:
            f.write(sample_XML_file)
        yield temp_csv_file


def test_resetJsonDict():
    result = resetJsonDict()

    assert isinstance(result, dict)
    assert result["_id"] is None
    assert result["Date"] is None


def test_check_if_json_file_exits():
    with TemporaryDirectory() as temp_dir:
        temp_xml_file = os.path.join(temp_dir, "input.xml")
        with open(temp_xml_file, "w") as f:
            f.write(sample_XML_file)
        
        main(temp_xml_file, "prueba")
        assert os.path.exists("mnt/shared/output.json")
