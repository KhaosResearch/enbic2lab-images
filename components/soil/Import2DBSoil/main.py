import glob
from zipfile import ZipFile
import argparse
import os
import numpy as np
import pandas as pd
import pygeodesy as geo
from minio import Minio
from pymongo import MongoClient
from dotenv import load_dotenv

def initJsonDict():
    json_d = {
        "Author": "Undefined",
        "_id": None,
        "Latitude": None,
        "Longitude": None,
        "Altitude": None,
        "Natural_Site": None,
        "SSC_Photo_Path": [],
        "Env_photo_path": [],
        "Incidence": None,
        "SSC_1": None,
        "Project": None,
        "Spectral_Response_Path": [],
        "Orientation": None,
        "Slope": None,
        "Uses2": None,
        "Uses3": None,
        "Lithology": None,
        "Gravels": None,
        "Very_Coarse_Sands": None,
        "Coarse_Sands": None,
        "Medium_Sands": None,
        "Fine_Sands": None,
        "Very_Fine_Sands": None,
        "Total_Sands": None,
        "Coarse_Silts": None,
        "Fine_Silts": None,
        "Total_Silts": None,
        "Clays": None,
        "Texture_Class": None,
        "Texture_Class_Julian": None,
        "K_Factor": None,
        "Apparent_Density": None,
        "Aggregate_Stability": None,
        "Permeability": None,
        "Field_Capacity": None,
        "Permanent_Wilting_Point": None,
        "Hydrophobicity": None,
        "Organic_Carbon": None,
        "C_Factor": None,
        "Organic_Matter": None,
        "Useful_Water": None,
        "pH": None,
        "Electric_Conductivity": None,
        "Group": "Soil",
        "Date": "Undefined",
    }

    return json_d



def main(
    filepath: str,
    compressed_file: str,
    compressed_file2: str
):
    load_dotenv()
    client = Minio(
        endpoint=os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY")
    )

    c = MongoClient(
        os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_ACCESS_KEY"),
    )
    db = c[os.getenv("MONGO_DATABASE")]
    collection = db[os.getenv("MONGO_COLLECTION")]

    data = pd.read_excel(filepath)
    data = data.replace({np.nan: None})

    with ZipFile(compressed_file, "r") as zip_ref:
        zip_ref.extractall("/mnt/shared/")
    zip_folder = compressed_file.split(".zip", 1)[0]

    with ZipFile(compressed_file2, "r") as zip_ref2:
        zip_ref2.extractall("/mnt/shared/")
    zip_folder2 = compressed_file2.split(".zip", 1)[0]

    set_json = []
    for i in data.index:
        new_json = initJsonDict()
        if len(str(data["_id"][i])) < 4:
            muestra = "0" + str(data["_id"][i])
        else:
            muestra = str(data["_id"][i])

        new_json["_id"] = muestra

        u = geo.Utm(
            30, "N", int(data["X_Coordinates"][i]), int(data["Y_Coordinates"][i])
        )
        x = u.toLatLon()
        new_json["Latitude"] = x[0]
        new_json["Longitude"] = x[1]
        new_json["Altitude"] = data["Altitude"][i]
        new_json["Natural_Site"] = data["Natural_Site"][i]
        new_json["SSC_Photo_Path"] = []
        new_json["Incidence"] = data["Incidence"][i]
        new_json["SSC_1"] = data["SSC-1"][i]
        new_json["Project"] = data["Project"][i]
        new_json["Spectral_Response_Path"] = []
        new_json["Env_photo_path"] = []
        new_json["Orientation"] = data["Orientation"][i]
        new_json["Slope"] = data["Slope"][i]
        new_json["Uses2"] = data["Uses2"][i]
        new_json["Uses3"] = data["Uses3"][i]
        new_json["Lithology"] = data["Lithology"][i]
        new_json["Gravels"] = data["Gravels"][i]
        new_json["Very_Coarse_Sands"] = data["Very_Coarse_Sands"][i]
        new_json["Coarse_Sands"] = data["Coarse_Sands"][i]
        new_json["Medium_Sands"] = data["Medium_Sands"][i]
        new_json["Fine_Sands"] = data["Fine_Sands"][i]
        new_json["Very_Fine_Sands"] = data["Very_Fine_Sands"][i]
        new_json["Total_Sands"] = data["Total_Sands"][i]
        new_json["Coarse_Silts"] = data["Coarse_Silts"][i]
        new_json["Fine_Silts"] = data["Fine_Silts"][i]
        new_json["Total_Silts"] = data["Total_Silts"][i]
        new_json["Clays"] = data["Clays"][i]
        new_json["Texture_Class"] = data["Texture_Class"][i]
        new_json["Texture_Class_Julian"] = data["Texture_Class_Julian"][i]
        new_json["K_Factor"] = data["K_Factor"][i]
        new_json["Apparent_Density"] = data["Apparent_Density"][i]
        new_json["Aggregate_Stability"] = data["Aggregate_Stability"][i]
        new_json["Permeability"] = data["Permeability"][i]
        new_json["Field_Capacity"] = data["Field_Capacity"][i]
        new_json["Permanent_Wilting_Point"] = data["Permanent_Wilting_Point"][i]
        new_json["Hydrophobicity"] = data["Hydrophobicity"][i]
        new_json["Organic_Carbon"] = data["Organic_Carbon"][i]
        new_json["C_Factor"] = data["C_Factor"][i]
        new_json["Organic_Matter"] = data["Organic_Matter"][i]
        new_json["Useful_Water"] = data["Useful_Water"][i]
        new_json["pH"] = data["pH"][i]
        new_json["Electric_Conductivity"] = data["Electric_Conductivity"][i]
        new_json["Group"] = "Soil"
        new_json["Author"] = "Undefined"
        new_json["Date"] = "Undefined"

        for file in glob.glob(zip_folder + "/" + muestra + "*"):
            if "A" in file.split("/", 2)[2]:
                path = "soil/" + muestra + "/pictures/ssc/" + file.split("/", 2)[2]
                client.fput_object("enbic2lab", path, file)
                new_json["SSC_Photo_Path"].append("enbic2lab/" + path)
            else:
                path = "soil/" + muestra + "/pictures/env/" + file.split("/", 2)[2]
                client.fput_object("enbic2lab", path, file)
                new_json["Env_photo_path"].append("enbic2lab/" + path)
        for file2 in glob.glob(zip_folder2 + "/" + muestra + "*"):
            path = "soil/" + muestra + "/spectral/" + file2.split("/", 2)[2]
            client.fput_object("enbic2lab", path, file2)
            new_json["Spectral_Response_Path"].append("enbic2lab/" + path)

        set_json.append(new_json)
        i += 1

    for element in set_json:
        try:
            collection.update_one(
                {"_id": element["_id"]}, {"$set": element}, upsert=True
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import a JSON File to a MongoDB database."
    )
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/parques_naturales.xlsx",
        help="XLSX file path.",
    )
    parser.add_argument(
        "--compressed-file",
        type=str,
        default="/mnt/shared/lifewatch-prueba.zip",
        help="Compressed images file path.",
    )
    parser.add_argument(
        "--compressed-file2",
        type=str,
        default="/mnt/shared/Espectro.zip",
        help="Compressed spectro file path.",
    )



    args = parser.parse_args()

    main(
        args.filepath,
        args.compressed_file,
        args.compressed_file2
    )
