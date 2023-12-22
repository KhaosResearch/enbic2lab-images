import argparse
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def main(filepath: str, delimiter: str, output1: str, output2: str, min_support: float = 0.2, min_threshold: float = 0.7):
    # Load data from a CSV file
    data = pd.read_csv(filepath, delimiter=delimiter, index_col=0)

    # Find the index where "Species" appears
    species_index_number = data.index.get_loc("Species")

    # Extract data for species
    data_spec = data.iloc[species_index_number + 1 :].T

    # Replace '-' with column names
    for column in data_spec:
        data_spec.loc[data_spec[column] != "-", column] = column

    # Join column values into a single string
    data_process = data_spec[list(data_spec.columns)].T.agg(",".join)
    data_process = pd.DataFrame(data_process)

    # Split the joined values into a list
    species_list = list(data_process[0].apply(lambda x: x.split(",")))

    # Encode the data as a binary matrix
    trans_encoder = TransactionEncoder()
    data_encoder = trans_encoder.fit(species_list).transform(species_list)
    data_encoded = pd.DataFrame(data_encoder, columns=trans_encoder.columns_)

    # Replace False values with 0 and drop the '-' column
    data_encoded = data_encoded.replace(False, 0)
    data_encoded = data_encoded.drop(columns=["-"])

    # Apply Apriori algorithm to find frequent itemsets
    data_priori = apriori(data_encoded.astype("bool"), min_support=min_support, use_colnames=True)

    # Apply association rules to find association between itemsets
    data_association = association_rules(data_priori, metric="confidence", min_threshold=min_threshold)

    # Convert itemsets to comma-separated strings and save to output1
    data_priori["itemsets"] = data_priori["itemsets"].apply(lambda x: ", ".join(list(x))).astype("unicode")
    data_priori.to_csv(output1, sep=delimiter)

    # Convert antecedents and consequents to comma-separated strings and save to output2
    data_association["antecedents"] = data_association["antecedents"].apply(lambda x: ", ".join(list(x))).astype("unicode")
    data_association["consequents"] = data_association["consequents"].apply(lambda x: ", ".join(list(x))).astype("unicode")
    data_association.to_csv(output2, sep=delimiter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fidelity Species Index")

    # Define command-line arguments
    parser.add_argument("--filepath", type=str, required=True, help="Filepath for the input CSV File")
    parser.add_argument("--delimiter", type=str, required=True, help="Delimiter of the classes in the input CSV File")
    parser.add_argument("--min_support", type=float, required=True, help="Min support")
    parser.add_argument("--min_threshold", type=float, required=True, help="Min threshold")
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

    # Call the main function with provided arguments and default output file paths
    main(args.filepath, args.delimiter, args.output +"/support.csv", args.output + "/support_predict.csv", args.min_support, args.min_threshold)