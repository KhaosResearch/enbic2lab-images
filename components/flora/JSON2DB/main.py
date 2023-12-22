import argparse
import json
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

key_mapping = {"floras_samples": "ENBIC2ID", "floras_taxones": "specieName"}


def main(filepath: str, collection_name: str, collision_policy: str) -> None:
    """
    Read data from a JSON file and insert or update documents in a MongoDB collection.

    Args:
        filepath: The path to the JSON file.
        collection_name: The name of the MongoDB collection.
        collision_policy: The collision policy for handling existing documents.

    Returns:
        None
    """
    # Connect to the MongoDB server
    client = MongoClient(
        os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_ACCESS_KEY"),
    )

    # Access the specified database and collection
    db = client.get_database(os.getenv("MONGO_DATABASE"))
    collection = db.get_collection(collection_name)

    # Read the data from the JSON file
    with open(filepath) as f:
        data = json.load(f)

        # Iterate over each document in the data
        for doc in data:
            # Set the _id field of the document based on the collection name
            doc["_id"] = doc[key_mapping[collection_name]]

            # Check if the document already exists in the collection
            if collection.find_one({"_id": doc["_id"]}):
                # Handle the collision based on the specified policy
                if collision_policy == "replace":
                    collection.replace_one({"_id": doc["_id"]}, doc)
            else:
                # Insert the document into the collection
                collection.insert_one(doc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload the json provided as input to a database."
    )
    parser.add_argument(
        "--filepath",
        type=str,
        help="Input JSON file path.",
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        help="Collection name.",
        choices=["floras_samples", "floras_taxones"],
    )
    parser.add_argument(
        "--collision-policy",
        type=str,
        help="Collision policy.",
        choices=["replace", "ignore"],
    )

    args = parser.parse_args()

    main(args.filepath, args.collection_name, args.collision_policy)
