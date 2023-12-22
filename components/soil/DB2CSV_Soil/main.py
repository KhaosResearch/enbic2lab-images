from re import findall
from typing import Collection, List

import pandas as pd
import pymongo
import os

from argparse import ArgumentParser

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_ACCESS_KEY = os.environ["MONGO_ACCESS_KEY"]
MONGO_DB = os.environ["MONGO_DB"]
MONGO_COLLECTION = os.environ["MONGO_COLLECTION"]

def parse_author(authors: List[str]) -> List[str] | None:
    """Parse a list of author names for MongoDB query.

    This function takes a list of author names and creates a query condition that can be used in a MongoDB query. The condition searches for documents with author names that match any of the names in the list.

    Args:
        authors (List[str]): A list of author names to be used in the query condition.

    Returns:
        List[str] or None: A MongoDB query condition that searches for documents with author names matching any of the names in the provided list. Returns None if the list is empty or contains only empty or "[]" values.

    Example:
        To create a MongoDB query condition for author names "Author1" and "Author2":

        >>> query_condition = __parse_author(["Author1", "Author2"])

    Note:
        - This function is used internally to create a MongoDB query condition for author names based on user input.
    """
    author_query = [
        {"Author": {"$regex": a, "$options": "i"}} for a in authors if a and a != "[]"
    ]
    if author_query:
        if len(author_query) > 1:
            return {"$or": author_query}
        else:
            return author_query[0]
    return None


def parse_natural_site(natural_site_list: List[str]) -> List[str] | None:
    """Parse a list of natural site names for MongoDB query.

    This function takes a list of natural site names and creates a query condition that can be used in a MongoDB query. The condition searches for documents with natural site names that match any of the names in the list.

    Args:
        natural_site_list (List[str]): A list of natural site names to be used in the query condition.

    Returns:
        List[str] or None: A MongoDB query condition that searches for documents with natural site names matching any of the names in the provided list. Returns None if the list is empty or contains only empty or "[]" values.

    Example:
        To create a MongoDB query condition for natural site names "SiteA" and "SiteB":

        >>> query_condition = __parse_natural_site(["SiteA", "SiteB"])

    Note:
        - This function is used internally to create a MongoDB query condition for natural site names based on user input.
    """
    natural_site_query = [
        {"Natural_Site": {"$regex": s, "$options": "i"}}
        for s in natural_site_list
        if s and s != "[]"
    ]
    if natural_site_query:
        if len(natural_site_query) > 1:
            return {"$or": natural_site_query}
        else:
            return natural_site_query[0]
    return None


def mongo_connection_to_collection() -> Collection:
    """Connect to a MongoDB database and collection.

    This function connects to a MongoDB database and collection using the credentials stored in the .env file.

    Returns:
        mongo_col (Collection): A MongoDB collection object.

    Example:
        To connect to a MongoDB database and collection:

        >>> mongo_col = __mongo_connection_to_collection()

    Note:
        - This function is used internally to connect to a MongoDB database and collection.
    """
    mongo_client = pymongo.MongoClient(
        MONGO_HOST,
        username=MONGO_USERNAME,
        password=MONGO_ACCESS_KEY,
    )
    mongo_db = mongo_client[MONGO_DB]
    mongo_col = mongo_db[MONGO_COLLECTION]

    return mongo_col


def db2csv_soil(
    output: str,
    delimiter: str = ";",
    id: str = None,
    author: List[str] = None,
    description: str = None,
    natural_site_list: List[str] = None,
    project: str = None,
    start_date: str = None,
    end_date: str = None,
) -> None:
    """Query a MongoDB database and export the results to a CSV file with soil-related data.

    This function connects to a MongoDB database, performs a query based on specified parameters, and exports the query results to a CSV file with soil-related data.

    Args:
        output (str): The path to save the output CSV file.
        delimiter(str): The delimiter to use when saving the output CSV file. Default is ';'.
        id (str): Unique identifier for the soil data. Default is None.
        author (List[str]): List of authors associated with the soil data. Default is None.
        description (str): Description or keywords related to the soil data. Default is None.
        natural_site_list (List[str]): List of natural site names related to the soil data. Default is None.
        project (str): Project name or identifier associated with the soil data. Default is None.
        start_date (str): Start date for a time range filter. Default is None.
        end_date (str): End date for a time range filter. Default is None.

    Raises:
        KeyError: If no results are found for the given parameters in the MongoDB database.

    Example:
        To query a MongoDB database for soil-related data based on specified parameters and save the results in 'soil_data.csv':

        >>> db2csv_soil(
        >>>     output="soil_data.csv",
        >>>     delimiter=";",
        >>>     id="12345",
        >>>     author=["Author1", "Author2"],
        >>>     description="Soil analysis",
        >>>     natural_site_list=["SiteA", "SiteB"],
        >>>     project="ProjectX",
        >>>     start_date="2022-01-01",
        >>>     end_date="2022-12-31"
        >>> )
    """

    # Connect to the MongoDB database

    mongo_col = mongo_connection_to_collection()

    # Define a dictionary to map fields to conditions
    conditions = {
        "_id": lambda x: {"_id": x},
        "description": lambda x: {"Description": {"$regex": x, "$options": "i"}},
        "author": lambda x: parse_author(x),
        "natural_site_list": lambda x: parse_natural_site(x),
        "project": lambda x: {"Project": x},
        "start_date": lambda x: {"Date": {"$gte": pd.to_datetime(x, utc=True)}},
        "end_date": lambda x: {"Date": {"$lte": pd.to_datetime(x, utc=True)}},
    }

    # Create a list of queries based on input fields
    query_list = [
        conditions[field](value)
        for field, value in {
            "_id": id,
            "description": description,
            "author": author,
            "natural_site_list": natural_site_list,
            "project": project,
            "start_date": start_date,
            "end_date": end_date,
        }.items()
        if value
    ]

    # Query the database
    try:
        cursor = (
            mongo_col.find({"$and": query_list}) if query_list else mongo_col.find()
        )
    except TypeError as e:
        raise e

    # Create a dataframe with the results
    solid_output: pd.DataFrame = pd.DataFrame()

    # Iterate over the cursor and append the results to the dataframe
    for document in cursor:
        document.pop("_id")
        df_dictionary = pd.DataFrame([document])
        solid_output = pd.concat([solid_output, df_dictionary], ignore_index=True)

    # Check if the dataframe is empty and raise an error if it is empty or save the results to a csv file
    if solid_output.empty:
        raise KeyError("No results found for the given parameters")
    else:
        solid_output.to_csv(output, sep=delimiter, index=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="DB2CSV Soil")
    parser.add_argument(
        "--id",
        type=str,
        help="Identifier number of an especific sample",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--author",
        type=str,
        help="List of authors of the sample, separated by commas",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--description",
        type=str,
        help="Description of the sample",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--natural-site-list",
        dest="natural_site_list",
        type=str,
        help="List of natural sites of the sample, separated by commas",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Project name of the sample",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--start-date",
        dest="start_date",
        type=str,
        help="Start date for search samples by date range",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--end-date",
        dest="end_date",
        type=str,
        help="End date for search samples by date range",
        required=False,
        default=None,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter to use when saving the CSV file",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to save the output CSV file",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    args.natural_site_list = findall(r'\s*([^,]+)\s*', args.natural_site_list) if args.natural_site_list != None else None
    args.author = findall(r'\s*([^,]+)\s*', args.author) if args.author != None else None


    db2csv_soil(
        id=args.id,
        author=args.author,
        description=args.description,
        natural_site_list=args.natural_site_list,
        project=args.project,
        start_date=args.start_date,
        end_date=args.end_date,
        delimiter=args.delimiter,
        output=args.output+"/soil.csv",
    )
