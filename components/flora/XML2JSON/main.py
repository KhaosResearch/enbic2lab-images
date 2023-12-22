import argparse
import json
import re

import untangle


def resetJsonDict():
    json_D = {
        "_id": None,
        "Date": None,
        "Authors": [],
        "Group": "Flora",
        "Project": None,
        "Community": None,
        "Community_Authors": [],
        "Community_Year": None,
        "Subcommunity": None,
        "Subcommunity_Authors": [],
        "Subcommunity_Year": None,
        "Location": None,
        "MGRS": None,
        "Natural_Site": None,
        "Lithology": None,
        "Coverage": None,
        "Altitude": None,
        "Plot_Slope": None,
        "Alt_Veg": None,
        "Plot_Area": None,
        "Plot_Orientation": None,
        "Ecology": None,
        "Species": [],
        "Pictures": [],
    }

    return json_D


def indTransform(index):
    ind = ""
    if index == "(+)":
        ind = "+"
    elif index == "+.2":
        ind = "+"
    elif index == ".":
        ind = "-"
    elif index == "x":
        ind = "-"
    elif index == "X":
        ind = "-"
    elif index == "r":
        ind = "+"
    elif len(index) == 3:
        ind = index[0]
    else:
        ind = index
    return ind


def main(filepath: str, natural_site: str, output: str):
    doc = untangle.parse(filepath)
    author_list = " "
    subcom = " "
    subcom_author = " "
    json_list = []
    register_list = []
    separator = " "

    for rel in doc.ReleveTable.Releve:
        json_dict = resetJsonDict()
        if rel["name"] not in register_list:
            json_dict["_id"] = rel["name"]
            json_dict["Natural_Site"] = natural_site.replace("_", " ")
            json_dict["Plot_Area"] = float(rel.PlotArea.cdata)
            json_dict["MGRS"] = rel.CitationCoordinate["code"]

            if hasattr(rel, "OriginalSyntaxonName") == True:
                interest_community = re.split(
                    " subass. ", rel.OriginalSyntaxonName.cdata
                )
                community = re.split(" ", interest_community[0])
                found = False
                for word in community:
                    if found == False:
                        if word.endswith(
                            (
                                "etea",
                                "etalia",
                                "enalia",
                                "ion",
                                "enion",
                                "etum",
                                "etosum",
                            )
                        ):
                            word_index = community.index(word) + 1
                            if community[word_index] != "in" and "etum" in word:
                                com = separator.join(
                                    community[0 : word_index + 1]
                                ).strip()
                                aut = author_list.join(
                                    community[word_index + 1 : -1]
                                ).strip()
                            else:
                                com = separator.join(community[0:word_index]).strip()
                                aut = author_list.join(community[word_index:-1]).strip()
                            list_authors = re.split(" nom.", aut)
                            if "nom." in aut:
                                list_date = list_authors[0].split(" ")
                                if str.isdigit(list_date[-1]):
                                    json_dict["Community_Year"] = int(list_date[-1])
                                    new_authors = list_date[0:-1]
                                    list_authors[0] = " ".join(new_authors)
                                else:
                                    list_date = list_authors[1].split(" ")
                                    if str.isdigit(list_date[-1]):
                                        json_dict["Community_Year"] = int(list_date[-1])
                                        new_authors = list_date[0:-1]
                                        list_authors[1] = " ".join(new_authors)
                            final_list_authors = " ".join(list_authors)
                            authors = final_list_authors.replace("(", ",")
                            authors_final = authors.replace(")", ",")
                            auth = re.split(
                                r"; | & |, | ,| et | y | ex | em. | corr. |in ",
                                authors_final,
                            )
                            for author in auth:
                                author_updated = author.strip()
                                auth_updated = author_updated.strip(",")
                                if (
                                    auth_updated not in json_dict["Community_Authors"]
                                    and str.isdigit(auth_updated) == False
                                    and auth_updated != "al."
                                    and "col." not in auth_updated
                                    and "cols." not in auth_updated
                                    and auth_updated != ""
                                ):
                                    json_dict["Community_Authors"].append(auth_updated)
                            found = True
                if found == False:
                    if community[0] == "Comunidad":
                        if len(community) > 4 and community[4] == "y":
                            if community[7] == "subsp.":
                                com = separator.join(community[0:9]).strip()
                                final_list_authors = " ".join(community[9:-1])
                                auth = re.split(
                                    r"; | & |, | ,| et | y | ex | em. | corr. |in ",
                                    final_list_authors,
                                )
                                for author in auth:
                                    auth_updated = author.strip()
                                    if (
                                        auth_updated
                                        not in json_dict["Community_Authors"]
                                        and str.isdigit(auth_updated) == False
                                        and auth_updated != "al."
                                        and "col." not in auth_updated
                                        and "cols." not in auth_updated
                                        and auth_updated != ""
                                        and auth_updated != "*"
                                    ):
                                        json_dict["Community_Authors"].append(
                                            auth_updated
                                        )
                            else:
                                com = separator.join(community[0:7]).strip()
                                final_list_authors = " ".join(community[7:-1])
                                auth = re.split(
                                    r"; | & |, | ,| et | y | ex | em. | corr. |in ",
                                    final_list_authors,
                                )
                                for author in auth:
                                    auth_updated = author.strip()
                                    if (
                                        auth_updated
                                        not in json_dict["Community_Authors"]
                                        and str.isdigit(auth_updated) == False
                                        and auth_updated != "al."
                                        and "col." not in auth_updated
                                        and "cols." not in auth_updated
                                        and auth_updated != ""
                                        and auth_updated != "*"
                                    ):
                                        json_dict["Community_Authors"].append(
                                            auth_updated
                                        )
                        elif len(community) > 4 and community[4] == "subsp.":
                            com = separator.join(community[0:6]).strip()
                            final_list_authors = " ".join(community[6:-1])
                            auth = re.split(
                                r"; | & |, | ,| et | y | ex | em. | corr. |in ",
                                final_list_authors,
                            )
                            for author in auth:
                                auth_updated = author.strip()
                                if (
                                    auth_updated not in json_dict["Community_Authors"]
                                    and str.isdigit(auth_updated) == False
                                    and auth_updated != "al."
                                    and "col." not in auth_updated
                                    and "cols." not in auth_updated
                                    and auth_updated != ""
                                    and auth_updated != "*"
                                ):
                                    json_dict["Community_Authors"].append(auth_updated)
                        else:
                            com = separator.join(community[0:4]).strip()
                            final_list_authors = " ".join(community[4:-1])
                            auth = re.split(
                                r"; | & |, | ,| et | y | ex | em. | corr. |in ",
                                final_list_authors,
                            )
                            for author in auth:
                                auth_updated = author.strip()
                                if (
                                    auth_updated not in json_dict["Community_Authors"]
                                    and str.isdigit(auth_updated) == False
                                    and auth_updated != "al."
                                    and "col." not in auth_updated
                                    and "cols." not in auth_updated
                                    and auth_updated != ""
                                ):
                                    json_dict["Community_Authors"].append(auth_updated)
                        if str.isdigit(community[-1]):
                            json_dict["Community_Year"] = int(community[-1])
                    else:
                        if str.isdigit(community[-1]):
                            com = separator.join(community[:-1]).strip()
                        elif community[-1] == "**":
                            com = separator.join(community[:-1]).strip()
                        else:
                            com = separator.join(community).strip()
                else:
                    if str.isdigit(community[-1]):
                        json_dict["Community_Year"] = int(community[-1])
                    else:
                        pass
                json_dict["Community"] = com

                if len(interest_community) > 1:
                    subcommunity = re.split(" ", interest_community[1])
                    json_dict["Subcommunity"] = subcom.join(subcommunity[0:2]).strip()
                    if len(subcommunity) > 2:
                        if subcommunity[2] != "*":
                            if str.isdigit(subcommunity[-1]) == False:
                                subcom_aut = subcom_author.join(
                                    subcommunity[2:]
                                ).strip()
                            else:
                                subcom_aut = subcom_author.join(
                                    subcommunity[2:-1]
                                ).strip()
                            subcom_authors = subcom_aut.replace("(", ",")
                            subcom_authors_final = subcom_authors.replace(")", ",")
                            subcom_auth = re.split(
                                r"; | & |, | et | y | in | ex | em. | corr. ",
                                subcom_authors_final,
                            )
                            for author in subcom_auth:
                                author_updated = author.strip()
                                auth_updated = author_updated.strip(",")
                                if (
                                    auth_updated
                                    not in json_dict["Subcommunity_Authors"]
                                    and str.isdigit(auth_updated) == False
                                    and "al." not in auth_updated
                                    and "col." not in auth_updated
                                    and "cols." not in auth_updated
                                    and auth_updated != ""
                                ):
                                    json_dict["Subcommunity_Authors"].append(
                                        auth_updated
                                    )
                    if str.isdigit(subcommunity[-1]):
                        json_dict["Subcommunity_Year"] = int(subcommunity[-1])
            else:
                pass
            if hasattr(rel.SideData[1], "Datum"):
                for sd1 in rel.SideData[1].Datum:
                    if sd1["label"] == "Locality":
                        json_dict["Location"] = (
                            sd1.value.cdata.replace("Â¡", "Ã­")
                            .replace("\u00a6", ".")
                            .replace("Â¢", "Ã³")
                            .replace("\u00a0", "a")
                            .replace("\u00a3", "u")
                            .replace("Â¤", "Ã±")
                            .replace("Â®Ã¿", "")
                            .replace("Âµ", "a")
                        )
                    elif sd1["label"] == "Altitude":
                        try:
                            json_dict["Altitude"] = float(sd1.value.cdata)
                        except:
                            pass

                    elif sd1["label"] == "Inclination":
                        try:
                            json_dict["Plot_Slope"] = float(sd1.value.cdata)
                        except:
                            pass

                    elif sd1["label"] == "Aspect":
                        try:
                            json_dict["Plot_Orientation"] = sd1.value.cdata
                        except:
                            pass

            if hasattr(rel.SideData[2], "Datum"):
                for sd2 in rel.SideData[2].Datum:
                    if sd2["label"] == "Total Cover (%)":
                        try:
                            json_dict["Coverage"] = float(sd2.value.cdata)
                        except:
                            pass
                    elif sd2["label"] == "Shrub Height (m)":
                        try:
                            json_dict["Alt_Veg"] = float(sd2.value.cdata)
                        except:
                            pass

            if hasattr(rel, "ReleveEntry"):
                for sp in rel.ReleveEntry:
                    if sp["accepted_name"]:
                        if "subsp." in sp["accepted_name"]:
                            specie_array = sp["accepted_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0]
                                    + " "
                                    + specie_array[1]
                                    + " "
                                    + specie_array[specie_array.index("subsp.")]
                                    + " "
                                    + specie_array[specie_array.index("subsp.") + 1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
                        elif "var." in sp["accepted_name"]:
                            specie_array = sp["accepted_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0]
                                    + " "
                                    + specie_array[1]
                                    + " "
                                    + specie_array[specie_array.index("var.")]
                                    + " "
                                    + specie_array[specie_array.index("var.") + 1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
                        else:
                            specie_array = sp["accepted_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0] + " " + specie_array[1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
                    else:
                        if "subsp." in sp["original_name"]:
                            specie_array = sp["original_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0]
                                    + " "
                                    + specie_array[1]
                                    + " "
                                    + specie_array[specie_array.index("subsp.")]
                                    + " "
                                    + specie_array[specie_array.index("subsp.") + 1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
                        elif "var." in sp["original_name"]:
                            specie_array = sp["original_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0]
                                    + " "
                                    + specie_array[1]
                                    + " "
                                    + specie_array[specie_array.index("var.")]
                                    + " "
                                    + specie_array[specie_array.index("var.") + 1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
                        else:
                            specie_array = sp["original_name"].split(" ")
                            json_dict["Species"].append(
                                {
                                    "Name": specie_array[0] + " " + specie_array[1],
                                    "Ind": indTransform(sp["value"]),
                                }
                            )
            json_list.append(json_dict)
        else:
            pass

    with open(output, "w", encoding="utf8") as f:
        f.write(json.dumps(json_list, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a XML file to a standar flora JSON file."
    )
    parser.add_argument(
        "--filepath", type=str, default="30STF66.1.xml", help="XML file path."
    ),
    parser.add_argument(
        "--natural-site", type=str, default="Sierra Morena", help="Natural Site name."
    )
    args = parser.parse_args()

    main(args.filepath, args.natural_site, "/mnt/shared/output.json")
