import argparse

import pandas as pd
from pyvis.network import Network
import re


def neighbors_species(df, list_species):
    """
    Given a dataframe and a list of species, returns a dictionary with the neighbors of each species in the list.

    Parameters:
    df (pd.DataFrame): The dataframe containing the species and their connections.
    list_species (List[str]): The list of species to find neighbors for.

    Returns:
    Dict[str, Dict[str, int]]: A dictionary where the keys are the species in the list and the values are dictionaries
    containing the neighbors of each species and their connection strength.
    """
    list_species_all = []
    dict_species = {}

    for species in list_species:
        # Extract all forms where the species is listed and create a new dataframe
        list_species_for_speceis = []
        resultados = df[df[species] != "-"]
        # Extract all species from the forms where the species is present (grade 1)
        for index, row in resultados.iterrows():
            for columna in resultados.columns:
                if row[columna] != "-":
                    list_species_all.append(columna)
                    list_species_for_speceis.append(columna)
        # Save the species and their neighbors in a dictionary to facilitate the creation of the 'from', 'to' graph
        dict_species.update({species: list(set(list_species_for_speceis))})

    # Store dict_species for graph creation and neighbors_grado for the next degree
    neighbors = list(set(list_species_all))
    neighbors_grado = [x for x in neighbors if x not in list_species]
    result = [dict_species, neighbors_grado]
    return result


def add_node_and_edge(g_c, specie: str, dit_species: dict, grade: int):
    """
    Given a network graph object, a target species, a dictionary of neighbors and their connection strength, and a grade,
    adds the target species and its neighbors to the graph with the given grade.

    Parameters:
    g_c (Network): The network graph object to add the nodes and edges to.
    species_target (str): The target species to add to the graph.
    diciona_de_grado (Dict[str, int]): A dictionary where the keys are the neighbors of the target species and the values
    are the connection strength between the target species and its neighbors.
    grado (int): The grade of the target species in the graph.
    """
    if not specie in g_c.nodes:
        g_c.add_node(specie, label=specie, title=specie + ", Path: " + specie, size=100)

    node_ids = [node["id"] for node in g_c.nodes]
    for key in dit_species:
        if not key in node_ids:

            info_node = g_c.get_node(specie)
            patron = r"Path: [^']*"
            path = re.search(patron, str(info_node))
            title = (
                "Specie: "
                + key
                + "\n"
                + "Path: "
                + path.group(0).replace("Path: ", "")
                + " -> "
                + key
            )

            g_c.add_node(key, label=key, title=title, size=50)
            if str(specie) != str(key):
                g_c.add_edge(specie, key, title="Grado: " + str(grade), value=2)


def main(filepath: str, species: str, grade: int, output: str):
    """
    Given a filepath to a csv file containing species and their connections, a target species, and a grade, creates a
    network graph of the target species and its neighbors up to the given grade and saves it as an html file. Also saves
    the graph data as a csv file.

    Parameters:
    filepath (str): The filepath to the csv file containing the species and their connections.
    species (str): The target species to create the graph for.
    grade (int): The maximum grade of neighbors to include in the graph.
    """
    grade = int(grade)
    g_c = Network(
        "1600px", "100%", select_menu=True, cdn_resources="remote"
    )  # select_menu=True//filter_menu=True

    g_c.set_options(
        """
            "var options ="{
                "nodes": { 
                    "color": {
                        "hover": {
                            "border": "rgba(231,44,233,1)"
                        }
                    },
                    "shape": "dot"
                },
                "edges": {
                    "arrowStrikethrough": false,
                    "color": {
                        "highlight": "rgb(255, 0, 0)",
                        "hover": "rgba(128,25,132,1)",
                        "inherit": false
                    },
                    "smooth": {
                        "type": "vertical",
                        "forceDirection": "none"
                    }
                },
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -80000,
                        "springLength": 250,
                        "springConstant": 0.001
                    },
                    "minVelocity": 0.75
                }
            }"""
    )
    old_species = 0
    try:
        data = pd.read_csv(filepath, delimiter=";", index_col=0)
        species_index_number = data.index.get_loc("Species")

        data_spec = data.iloc[species_index_number + 1 :]
        df = data_spec.T

        list_species = [species]
        all_species = df.columns.tolist()

        dict_grade = {}
        num_jamps = 0

        # Create a dictionary with the degrees and their neighbors
        while grade != 0:
            num_jamps += 1

            list_neighbors = neighbors_species(df, list_species)
            # list_neighbors[0] = dictionary for creating graph element:links // list_neighbors[1] = list of total species for the next degree
            dict_grade.update({num_jamps: list_neighbors[0]})
            if grade != 0:
                list_species = list_neighbors[1]
            grade -= 1
            # Emergency brake, if there are no more species to classify, set degree to 0
            all_species = [x for x in all_species if x not in list_neighbors[1]]

            if len(all_species) == 0:
                grade = 0
            if len(all_species) == old_species:
                grade = 0
            else:
                old_species = len(all_species)

        # Create a network graph object
        for grado, value in dict_grade.items():
            for species_target, diciona_de_grado in value.items():
                add_node_and_edge(g_c, species_target, diciona_de_grado, grado)

        output_html = output + "/output.html"
        g_c.write_html(output_html)

        # Create a CSV file to import the graph into Gephi or Neo4j
        list_from = []
        list_to = []
        list_grade = []
        for edge in g_c.edges:
            list_from.append(edge["from"])
            list_grade.append(edge["title"].replace("Grado: ", ""))
            if edge["to"]:
                list_to.append(edge["to"])

        data = {"from": list_from, "to": list_to, "grade": list_grade}
        df = pd.DataFrame(data)
        df.to_csv(output + "output.csv", index=False)
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fidelity grade Plot")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath for the input CSV File",
    )

    parser.add_argument(
        "--species",
        type=str,
        required=True,
        help="Target species",
    )
    parser.add_argument(
        "--grade",
        type=int,
        required=True,
        help="Maximum grade of neighbors to include in the graph",
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

    main(args.filepath, args.species, args.grade, args.output)
