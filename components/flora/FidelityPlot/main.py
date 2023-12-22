import argparse

import pandas as pd
from pyvis.network import Network


def main(filepath: str, delimiter: str, output: str):
    """
    Read a CSV file, create a network graph, and display it.

    Args:
        filepath (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.
        output (str): The output file name for the network graph.

    Returns:
        network: '/mnt/shared/output.html'
    """

    # Create a network graph object
    g_c = Network("1600px", "100%")

    # Read the CSV file
    df = pd.read_csv(filepath, delimiter=delimiter)
    df.drop([0])

    # Set the options for the network graph
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
                    "highlight": "rgba(132,48,51,1)",
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
                "minVelocity": 5
            }
        }"""
    )

    # Iterate through each row in the CSV file
    for row in df.itertuples():
        # If there is more than one species in the row, create edges between them
        if len(row.itemsets.split(", ")) != 1:
            for specie in row.itemsets.split(", "):
                # Add the species to the network graph if it doesn't already exist, excluding border itself
                if not specie in g_c.nodes:
                    g_c.add_node(specie, label=specie)
                n = 0
                while n != len(row.itemsets.split(", ")):
                    if specie != row.itemsets.split(", ")[n]:
                        if not specie in g_c.nodes:
                            g_c.add_node(
                                row.itemsets.split(", ")[n],
                                label=row.itemsets.split(", ")[n],
                            )
                        g_c.add_edge(
                            specie,
                            row.itemsets.split(", ")[n],
                            value=row.support * 2,
                            title="Fidelity = "
                            + str(round(row.support * 100, 2))
                            + "%",
                        )
                    n += 1

    # Get the adjacency list for the network graph
    neighbor_map = g_c.get_adj_list()

    # Add titles to each node in the network graph
    for node in g_c.nodes:
        node_name = node["label"]
        node_neighbors = list(neighbor_map[node["id"]])
        if node_name in node_neighbors:
            node_neighbors.remove(node_name)
        node["title"] = (
            node["label"] + " -> Relation with:\n" + "\n".join(node_neighbors)
        )

    # Write the network graph to an HTML file
    output_html = output
    g_c.write_html(output_html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fidelity Plot")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath for the input CSV File",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=True,
        help="Delimiter of the classes in the input CSV File",
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

    main(args.filepath, args.delimiter, args.output + "/output.html")
