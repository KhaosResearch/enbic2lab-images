import argparse
import json
import numpy as np

import pandas as pd


def main(filepath: str, output_folder: str) -> None:
    """
    Read an Excel file, extract specific columns, and save them as JSON files.

    Args:
        filepath (str): The path to the Excel file.
        output_folder (str): The path to the folder where the JSON files will be saved.
    """
    # Read the Excel file
    df = pd.read_excel(filepath)
    df = df.sort_values(['genus','species','taxonRank','infraspecificEpithet','gbifID'], ascending=False)

    #Obtener nombres columnas 
    column_list=[df.columns[2],df.columns[5],df.columns[6],df.columns[7],df.columns[8],df.columns[9],df.columns[16],df.columns[21],df.columns[0],df.columns[1],df.columns[2],df.columns[3],df.columns[4],df.columns[10],df.columns[11],df.columns[12],df.columns[13],df.columns[14],df.columns[15],
    df.columns[17],df.columns[18],df.columns[19],df.columns[20],df.columns[22],df.columns[23],df.columns[24],df.columns[25],df.columns[26],df.columns[27],df.columns[28],df.columns[29],df.columns[30],df.columns[31], df.columns[32]]
    # Crear listas con columnas
    gbifID_list=list(df[column_list[0]])
    kingdom_list=list(df[column_list[1]])
    phylum_list=list(df[column_list[2]])
    order_list=list(df[column_list[3]])
    class_list=list(df[column_list[4]])
    family_list=list(df[column_list[5]])
    scientificName_list=list(df[column_list[6]])
    countryCode_list=list(df[column_list[7]])
    ENBIC2ID_list=list(df[column_list[8]])
    NaturalSite_list=list(df[column_list[9]])
    NaturalSite_list = ["Alcornocales" if natural_site == "ALC" else
                        "Sierra de las Nieves" if natural_site == "SN" else
                        "Cabo de Gata" if natural_site == "CGN" else
                        natural_site
                        for natural_site in NaturalSite_list]
    gbifID_list=list(df[column_list[10]])
    institutionCode_list=list(df[column_list[11]])
    catalogNumber_list=list(df[column_list[12]])
    catalogNumber_array=np.array(df[column_list[12]])
    genus_list=list(df[column_list[13]])
    hib_list=list(df[column_list[14]])
    species_list=list(df[column_list[15]])
    taxonRank_list=list(df[column_list[16]])
    infraspecificEpithet_list=list(df[column_list[17]])
    aut_infra_list=list(df[column_list[18]])
    taxonRankInterpreted_list=list(df[column_list[19]])
    speciesInterpreted_list=list(df[column_list[20]])
    identifiedBy_list=list(df[column_list[21]])
    dateIdentified_list=list(df[column_list[22]])
    stateProvince_list=list(df[column_list[23]])
    locality_list=list(df[column_list[24]])
    decimalLatitude_list=list(df[column_list[25]])
    decimalLongitude_list=list(df[column_list[26]])
    UTM_list=list(df[column_list[27]])
    coordinateUncertaintyInMeters_list=list(df[column_list[28]])
    elevation_list=list(df[column_list[29]])
    recordedBy_list=list(df[column_list[30]])
    eventDate_list=list(df[column_list[31]])
    remarks_list=list(df[column_list[32]])
    aut_esp_list=list(df[column_list[33]])
    # Crear nombre especie
    id_list=[]
    id_nonRank_list=[]
    taxonRank_complete_list=[]
    taxonRank_acronym_list=[]
    for i in range(len(df)):
        id=df.iloc[i]['genus']+" "+df.iloc[i]['hib']+" "+df.iloc[i]['species']+" "+df.iloc[i]['taxonRank']+" "+df.iloc[i]['infraspecificEpithet']
        id=id.replace("_","")
        id=id.replace("species","")
        id=id.replace("genus","")
        id=id.replace("hib","")
        id=id.replace("  "," ")
        id=id.strip()
        id_list.append(id)

        id_nonRank=df.iloc[i]['genus']+" "+df.iloc[i]['hib']+" "+df.iloc[i]['species']+" "+df.iloc[i]['infraspecificEpithet']
        id_nonRank=id_nonRank.replace("_","")
        id_nonRank=id_nonRank.replace("species","")
        id_nonRank=id_nonRank.replace("genus","")
        id_nonRank=id_nonRank.replace("hib","")
        id_nonRank=id_nonRank.replace("  "," ")
        id_nonRank=id_nonRank.strip()
        id_nonRank_list.append(id_nonRank)

        if(taxonRank_list[i]=="genus"):
            taxonRank_complete_list.append("genus")
            taxonRank_acronym_list.append("_")
        elif(taxonRank_list[i]=="species"):
            taxonRank_complete_list.append("species")
            taxonRank_acronym_list.append("_")
        elif(taxonRank_list[i]=="subsp."):
            taxonRank_complete_list.append("subspecies")
            taxonRank_acronym_list.append(taxonRank_list[i])
        elif(taxonRank_list[i]=="var."):
            taxonRank_complete_list.append("variety")
            taxonRank_acronym_list.append(taxonRank_list[i])
        elif(taxonRank_list[i]=="f."):
            taxonRank_complete_list.append("form")
            taxonRank_acronym_list.append(taxonRank_list[i])
        else:
            taxonRank_complete_list.append("hib")
            taxonRank_acronym_list.append(hib_list[i])

    for i in range(len(df)-1):
        if id_list[i]==id_list[i+1]:
            if gbifID_list[i]==0:
                phylum_list[i]=phylum_list[i-1]
                order_list[i]=order_list[i-1]
                class_list[i]=class_list[i-1]
                family_list[i]=family_list[i-1]
        elif id_list[i]!=id_list[i+1] and id_list[i]==id_list[i-1]:
            if gbifID_list[i]==0:
                phylum_list[i]=phylum_list[i-1]
                order_list[i]=order_list[i-1]
                class_list[i]=class_list[i-1]
                family_list[i]=family_list[i-1]

    #Crear dataframe con campos y valores Taxones

    dict_taxon = { 
                "specieName":id_list,
                "genus":genus_list,
                "species":species_list,
                "taxonRank": taxonRank_complete_list,
                "taxonRankAcronym":taxonRank_acronym_list,
                "infraspecificEpithet":infraspecificEpithet_list,
                "kingdom":kingdom_list,
                "phylum":phylum_list,
                "order":order_list,
                "class":class_list,
                "family":family_list,
                "aut_esp":aut_esp_list
                }
    df_taxon=pd.DataFrame(data=dict_taxon)
    df_taxon_uniques=df_taxon.drop_duplicates()
    df_taxon_uniques=df_taxon_uniques.fillna("")
    df_taxon_uniques = df_taxon_uniques.sort_values('specieName', ascending=True)
    df_taxon_uniques=df_taxon_uniques[1:]

    # Save the selected columns as a JSON file
    df_taxon_uniques.to_json(
        f"{output_folder}/taxon.json", orient="records", indent=2
    )

    #Crear dataframe con campos y valores Muestras

    dict_samples = {"ENBIC2ID":ENBIC2ID_list,
                    "Natural_Site":NaturalSite_list,
                    "gbifID":gbifID_list,            
                    "institutionCode":institutionCode_list,
                    "catalogNumber":catalogNumber_list,
                    "scientificName":scientificName_list,
                    "aut_infra":aut_infra_list,
                    "taxonRankInterpreted":taxonRankInterpreted_list,
                    "speciesInterpreted":speciesInterpreted_list,
                    "identifiedBy":identifiedBy_list,
                    "dateIdentified":dateIdentified_list,
                    "countryCode":countryCode_list,
                    "stateProvince":stateProvince_list,
                    "locality":locality_list,
                    "Latitude":decimalLatitude_list,
                    "Longitude":decimalLongitude_list,
                    "coordinateUncertaintyInMeters":coordinateUncertaintyInMeters_list,
                    "elevation":elevation_list,
                    "recordedBy":recordedBy_list,
                    "eventDate":eventDate_list,
                    "remarks":remarks_list,
                    "UTM":UTM_list,
                    "specieName":id_list,
                    }
    df_samples=pd.DataFrame(data=dict_samples)
    df_samples = df_samples.sort_values('specieName')
    df_samples_uniques=df_samples.drop_duplicates()
    # Llenar valores nulos con cadena vacía, excepto para dateIdentified y eventDate
    columns_to_fill = df_samples_uniques.columns.difference(['dateIdentified', 'eventDate','coordinateUncertaintyInMeters'])
    df_samples_uniques[columns_to_fill] = df_samples_uniques[columns_to_fill].fillna('')
    df_samples_uniques_nan=df_samples_uniques[4:]

    df_samples_uniques_nan_order = df_samples_uniques_nan.sort_values('ENBIC2ID')
    # Guardar el DataFrame en un archivo JSON
    df_samples_uniques_nan_order.to_json(
        f"{output_folder}/sample.json",
        orient="records",
        indent=2,
        date_format="iso",  # Utiliza el formato ISO para las fechas
    )

    # Cargar el JSON y guardarlo nuevamente con ensure_ascii=False
    with open(f"{output_folder}/sample.json", 'r') as json_file:
        data = json.load(json_file)

    with open(f"{output_folder}/sample.json", 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates community statistics and species community"
    )
    parser.add_argument(
        "--filepath",
        type=str,
        help="Input XLSX file path.",
    )
    parser.add_argument(
        "--output-folder", type=str, help="Output folder path.", default="/mnt/shared"
    )
    args = parser.parse_args()

    main(
        args.filepath,
        args.output_folder,
    )
