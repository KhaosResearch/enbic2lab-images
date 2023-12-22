import argparse
import os
from typing import List, Optional

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def connect_to_DB():
    c = MongoClient(
        os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_ACCESS_KEY"),
    )
    db = c[os.getenv("MONGO_DATABASE")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    return collection

collection = connect_to_DB()

def check_presence(query: dict, error_message: str) -> None:
    count = collection.count_documents(query)
    if count == 0:
        raise ValueError(error_message)


def check_presence_for_list(items: List[str], field: str, error_message: str) -> None:
    if items and not all(elem == "" for elem in items):
        cnt = 0
        for element in items:
            if element != "":
                query = {field: {"$regex": element, "$options": "i"}}
                count = collection.count_documents(query)
                cnt += count

        if cnt == 0:
            raise ValueError(error_message)


def transform_to_dataframe(inventory_info):
    attributes_dict = {
        "No. of register (ID)": inventory_info["_id"],
        "Date": inventory_info["Date"],
        "Authors": ",".join(inventory_info["Authors"]),
        "Group": inventory_info["Group"],
        "Project": inventory_info["Project"],
        "Community": inventory_info["Community"],
        "Community Authors": ",".join(inventory_info["Community_Authors"]),
        "Community Year": inventory_info["Community_Year"],
        "Subcommunity": inventory_info["Subcommunity"],
        "Subcommunity Authors": ",".join(inventory_info["Subcommunity_Authors"]),
        "Subcommunity Year": inventory_info["Subcommunity_Year"],
        "Location": inventory_info["Location"],
        "MGRS": inventory_info["MGRS"],
        "Latitude": inventory_info["Latitude"],
        "Longitude": inventory_info["Longitude"],
        "Natural Site": inventory_info["Natural_Site"],
        "Lithology": inventory_info["Lithology"],
        "Coverage(%)": inventory_info["Coverage"],
        "Altitude(m)": inventory_info["Altitude"],
        "Plot slope": inventory_info["Plot_Slope"],
        "Alt. Veg. (cm)": inventory_info["Alt_Veg"],
        "Plot area(m2)": inventory_info["Plot_Area"],
        "Plot orientation": inventory_info["Plot_Orientation"],
        "Ecology": inventory_info["Ecology"],
        "Pictures": ",".join(inventory_info["Pictures"]),
        "Number of Species": sum(
            1 for specie in inventory_info["Species"] if specie["Ind"] != "-"
        ),
        "Species": "",
    }

    species_dict = {
        specie["Name"]: specie["Ind"] for specie in inventory_info["Species"]
    }

    return attributes_dict, species_dict


def generate_df(definitive_list):

    final_data_dicts = []
    unique_species_keys = set()
    for inventory_info in definitive_list:
        attributes_dict, species_dict = transform_to_dataframe(inventory_info)
        unique_species_keys.update(species_dict.keys())
        attributes_dict.update(species_dict)
        final_data_dicts.append(attributes_dict)

    df = pd.DataFrame(final_data_dicts).set_index("No. of register (ID)")

    species_columns = [col for col in df.columns if col in unique_species_keys]

    df[species_columns] = df[species_columns].fillna("-")

    final_dataframe = df.transpose()

    return final_dataframe


def main(
    start_date: Optional[int],
    end_date: Optional[int],
    community_start_year: Optional[int],
    community_end_year: Optional[int],
    subcommunity_start_year: Optional[int],
    subcommunity_end_year: Optional[int],
    project: Optional[str],
    natural_site: Optional[str],
    altitude: Optional[int],
    lithology: Optional[str],
    plot_orientation: Optional[str],
    plot_slope: Optional[str],
    phyto_index: Optional[str],
    num_species: Optional[int],
    community: Optional[List[str]],
    location: Optional[List[str]],
    author: Optional[List[str]],
    community_author: Optional[List[str]],
    subcommunity_author: Optional[List[str]],
    species: Optional[List[str]],
    output: str,
) -> None:

    final_list = []
    delimiter = ";"
    expr = []

    if project:
        check_presence(
            {"Project": {"$regex": project, "$options": "i"}},
            "Project '{}' is not present in inventories.".format(project),
        )

        expr.append({"Project": {"$regex": project, "$options": "i"}})

    if natural_site:
        check_presence(
            {"Natural_Site": {"$regex": natural_site, "$options": "i"}},
            "Natural Site '{}' is not present in inventories.".format(natural_site),
        )
        expr.append({"Natural_Site": {"$regex": natural_site, "$options": "i"}})

    if altitude:
        check_presence(
            {"Altitude": {"$eq": int(altitude)}},
            "Altitude '{}' is not present in inventories.".format(altitude),
        )
        expr.append({"Altitude": {"$eq": int(altitude)}})

    if lithology:
        check_presence(
            {"Lithology": {"$regex": lithology, "$options": "i"}},
            "Lithology '{}' is not present in inventories.".format(lithology),
        )
        expr.append({"Lithology": {"$regex": lithology, "$options": "i"}})

    if plot_orientation:
        check_presence(
            {"Plot_Orientation": {"$regex": plot_orientation, "$options": "i"}},
            "Plot Orientation '{}' is not present in inventories.".format(
                plot_orientation
            ),
        )
        expr.append({"Plot_Orientation": {"$regex": plot_orientation, "$options": "i"}})

    if plot_slope:
        check_presence(
            {"Plot_Slope": {"$eq": int(plot_slope)}},
            "Plot Slope '{}' is not present in inventories.".format(plot_slope),
        )
        expr.append({"Plot_Slope": {"$eq": float(plot_slope)}})

    if phyto_index:
        check_presence(
            {"Species.Ind": {"$eq": phyto_index}},
            "Phytosociological index '{}' is not present in inventories.".format(
                phyto_index
            ),
        )
        expr.append({"Species.Ind": {"$eq": phyto_index}})

    if location and not all(elem == "" for elem in location):
        check_presence_for_list(location, "Location", "No one location found.")
        location_exp = [
            {"Location": {"$regex": loc, "$options": "i"}} for loc in location
        ]
        if len(location_exp) > 1:
            expr.append({"$or": location_exp})
        elif len(location_exp) == 1:
            expr.append(location_exp[0])

    if author and not all(elem == "" for elem in author):
        check_presence_for_list(author, "Authors", "No one author found.")
        author_exp = [{"Authors": {"$regex": auth, "$options": "i"}} for auth in author]
        if len(author_exp) > 1:
            expr.append({"$or": author_exp})
        elif len(author_exp) == 1:
            expr.append(author_exp[0])

    if community and not all(elem == "" for elem in community):
        check_presence_for_list(community, "Community", "No community found.")
        community_exp = [
            {"Community": {"$regex": commu, "$options": "i"}} for commu in community
        ]
        if len(community_exp) > 1:
            expr.append({"$or": community_exp})
        elif len(community_exp) == 1:
            expr.append(community_exp[0])

    if community_author and not all(elem == "" for elem in community_author):
        check_presence_for_list(
            community_author, "Community_Authors", "No community author found."
        )

        author_exp = [
            {"Community_Authors": {"$regex": auth, "$options": "i"}} for auth in author
        ]
        if len(author_exp) > 1:
            expr.append({"$or": author_exp})
        elif len(author_exp) == 1:
            expr.append(author_exp[0])

    if subcommunity_author and not all(elem == "" for elem in subcommunity_author):
        check_presence_for_list(
            subcommunity_author,
            "Subcommunity_Authors",
            "No one subcommunity author found.",
        )
        author_exp = [
            {"Subcommunity_Authors": {"$regex": auth, "$options": "i"}}
            for auth in author
        ]
        if len(author_exp) > 1:
            expr.append({"$or": author_exp})
        elif len(author_exp) == 1:
            expr.append(author_exp[0])

    if species and not all(elem == "" for elem in species):
        check_presence_for_list(species, "Species.Name", "No one species found.")
        for particular_species in species:
            if len(particular_species) > 0:
                expr.append(
                    {"Species.Name": {"$regex": particular_species, "$options": "i"}}
                )

    if start_date and end_date:
        expr.append(
            {
                "Date": {
                    "$gte": pd.to_datetime(int(start_date), utc=True),
                    "$lte": pd.to_datetime(int(end_date), utc=True),
                }
            }
        )

    if start_date and not end_date:
        expr.append({"Date": {"$gte": pd.to_datetime(int(start_date), utc=True)}})

    if not start_date and end_date:
        expr.append({"Date": {"$lte": pd.to_datetime(int(end_date), utc=True)}})

    if community_start_year and community_end_year:
        expr.append(
            {
                "Community_Year": {
                    "$gt": int(community_start_year),
                    "$lt": int(community_end_year),
                }
            }
        )

    if community_start_year and not community_end_year:
        expr.append({"Community_Year": {"$gt": int(community_start_year)}})

    if not community_start_year and community_end_year:
        expr.append({"Community_Year": {"$lt": int(community_end_year)}})

    if subcommunity_start_year and subcommunity_end_year:
        expr.append(
            {
                "Subcommunity_Year": {
                    "$gt": int(subcommunity_start_year),
                    "$lt": int(subcommunity_end_year),
                }
            }
        )

    if subcommunity_start_year and not subcommunity_end_year:
        expr.append({"Subcommunity_Year": {"$gt": int(subcommunity_start_year)}})

    if not subcommunity_start_year and subcommunity_end_year:
        expr.append({"Subcommunity_Year": {"$lt": int(subcommunity_end_year)}})

    if expr:
        if len(expr) == 1:
            for result in collection.find(expr[0]):
                final_list.append(result)
        else:
            for result in collection.find({"$and": expr}):
                final_list.append(result)

    if expr == []:
        definitive_list = []
        for element in collection.find():
            definitive_list.append(element)
    else:
        definitive_list = final_list

    if definitive_list == []:
        raise ValueError("No inventory found for the given filters.")

    if num_species:
        list_species = []
        num = 0
        for filter_inventory in definitive_list:
            species = filter_inventory["Species"]
            cnt = 0
            for specie in species:
                if specie["Ind"] != "-":
                    cnt += 1
            if cnt == int(num_species):
                num += 1
                list_species.append(filter_inventory)
        definitive_list = list_species

    final_dataframe = generate_df(definitive_list)

    final_dataframe.to_csv(output, index_label="No. of register (ID)", sep=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get inventory flora data in CSV format via JSON collection filtering"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="",
        help="Initial date from which inventories are to be loaded",
    )

    parser.add_argument(
        "--end-date",
        type=str,
        default="",
        help="End date up to which inventories are to be loaded",
    )

    parser.add_argument(
        "--community-start-year",
        type=str,
        default="",
        help="Community initial year from which inventories are to be loaded",
    )

    parser.add_argument(
        "--community-end-year",
        type=str,
        default="",
        help="Community end year up to which inventories are to be loaded",
    )

    parser.add_argument(
        "--subcommunity-start-year",
        type=str,
        default="",
        help="Subcommunity initial year from which inventories are to be loaded",
    )

    parser.add_argument(
        "--subcommunity-end-year",
        type=str,
        default="",
        help="Subcommunity end year up to which inventories are to be loaded",
    )

    parser.add_argument("--project", type=str, default="", help="Project")
    parser.add_argument("--natural-site", type=str, default="", help="Natural Site")
    parser.add_argument("--altitude", type=str, default="", help="Altitude")
    parser.add_argument("--lithology", type=str, default="", help="Lithology")
    parser.add_argument(
        "--plot-orientation", type=str, default="", help="Plot Orientation"
    )
    parser.add_argument("--plot-slope", type=str, default="", help="Plot Slope")
    parser.add_argument(
        "--phyto-index", type=str, default="", help="Phytosociological index"
    )
    parser.add_argument("--num-species", type=str, default="", help="Number of species")

    parser.add_argument(
        "--community",
        type=str,
        nargs="*",
        default=[],
        help="List of communities to filter",
    )

    parser.add_argument(
        "--location",
        type=str,
        nargs="*",
        default=[],
        help="List of locations to filter",
    )

    parser.add_argument(
        "--author", type=str, nargs="*", default=[], help="List of authors to filter"
    )

    parser.add_argument(
        "--community-author",
        type=str,
        nargs="*",
        default=[],
        help="List of community authors to filter",
    )

    parser.add_argument(
        "--subcommunity-author",
        type=str,
        nargs="*",
        default=[],
        help="List of subcommunity authors to filter",
    )

    parser.add_argument(
        "--species", type=str, nargs="*", default=[], help="List of species to filter"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    main(
        args.start_date,
        args.end_date,
        args.community_start_year,
        args.community_end_year,
        args.subcommunity_start_year,
        args.subcommunity_end_year,
        args.project,
        args.natural_site,
        args.altitude,
        args.lithology,
        args.plot_orientation,
        args.plot_slope,
        args.phyto_index,
        args.num_species,
        args.community,
        args.location,
        args.author,
        args.community_author,
        args.subcommunity_author,
        args.species,
        args.output+"/output.csv",
    )
