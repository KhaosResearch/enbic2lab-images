import argparse
import json
import os
from datetime import datetime

import pygeodesy as geo
from pymongo import MongoClient

MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_DATABASE = os.environ["MONGO_DATABASE"]
MONGO_COLLECTION = os.environ["MONGO_COLLECTION"]

client = MongoClient(
    MONGO_HOST,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]


def main(filepath: str) -> None:
    f = open(filepath)
    data = json.load(f)

    duplicates = ""
    for d in data:
        duplicate = False
        input_species_list = []
        input_ind_list = []
        for species in d["Species"]:
            input_species_list.append(species["Name"])
            input_ind_list.append(species["Ind"])
        for result in collection.find({"Community_Year": d["Community_Year"]}):
            species_list = []
            ind_list = []
            for species in result["Species"]:
                species_list.append(species["Name"])
                ind_list.append(species["Ind"])
            if input_species_list == species_list and input_ind_list == ind_list:
                duplicate = True
                if duplicates == "":
                    duplicates = (
                        "The id "
                        + f'"{d["_id"]}"'
                        + " is duplicated, corresponding to the id "
                        + f'"{result["_id"]}"'
                        + " in the database."
                    )
                else:
                    duplicates = (
                        duplicates
                        + "\nThe id "
                        + f'"{d["_id"]}"'
                        + " is duplicated, corresponding to the id "
                        + f'"{result["_id"]}"'
                        + " in the database."
                    )
        if duplicate is False:
            cnt = 0
            for result in collection.find(
                {"_id": {"$regex": d["_id"], "$options": "i"}}
            ):
                cnt += 1
            if cnt != 0:
                raise ValueError(
                    "The number of register (ID) " + d["_id"] + " already exists."
                )
            else:
                if d["Date"] is not None:
                    d["Date"] = datetime.strptime(d["Date"], "%Y-%m-%d")
                if d["MGRS"] is not None:
                    e = geo.parseMGRS(d["MGRS"])
                    x = e.toLatLon()
                    d["Latitude"] = x[0]
                    d["Longitude"] = x[1]
                if d["MGRS"] is None:
                    d["Latitude"] = None
                    d["Longitude"] = None
                collection.update_one({"_id": d["_id"]}, {"$set": d}, upsert=True)

    if duplicates != "":
        print(
            "The following inventories haven't been import because they are duplicated: \n"
            + duplicates
        )

    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import a JSON File to a MongoDB database."
    )
    parser.add_argument(
        "--filepath", type=str, default="inventory.json", help="JSON file path."
    )
    args = parser.parse_args()

    main(args.filepath)
