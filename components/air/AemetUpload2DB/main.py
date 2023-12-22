import json
from datetime import datetime

import argparse
from pymongo import MongoClient

def main(filepath: str,user:str,password:str,path:str,database:str,collection:str):
    """
    Upload files dataset to mongoDB
    """

    # Connect to MongoDB
    c = MongoClient(path, username=user, password=password)
    db = c[database]
    collection = db[collection]

    # Read File
    f = open(filepath)
    json_data = json.load(f)

    # Upload File
    for data in json_data:
        data["fecha"] = datetime.strptime(data["fecha"], "%Y-%m-%d")
        collection.update_one({"fecha": data["fecha"]}, {"$set": data}, upsert=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima model")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/split_dataset.csv",
        required=True,
        help="File path of the JSON file",
    )
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="Username of MongoDB",
    )
    parser.add_argument(
        "--password",
        type=str,
        required=True,
        help="Password of MongoDB",
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Mongo Path of MongoDB",
    )
    parser.add_argument(
        "--database",
        type=str,
        required=True,
        help="Mongo Database",
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Mongo Collection of MongoDB",
    )
    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.user,
        args.password,
        args.path,
        args.database,
        args.collection
    )
