import pandas as pd
from pathlib import Path
import os
import argparse

# ================= METHODS =================


def createDataFrame(file_name, delimiter):
    if Path(file_name).suffix == ".csv" or Path(file_name).suffix == ".tsv":
        dataframe = pd.read_csv(file_name, delimiter=delimiter)
    else:
        raise Exception("Wrong extension. Only accept .csv files")
    return dataframe


def main(
    first_file_path: str,
    index_column_first_file: str,
    second_file_path: str,
    index_column_second_file: str,
    delimiter_file_1: str,
    delimiter_file_2: str,
    delimiter: str,
    join_how_parameter: str,
    output: str,
):
    
    dataframe_first_file = createDataFrame(first_file_path, delimiter_file_1)

    # Read second file
    dataframe_second_file = createDataFrame(second_file_path, delimiter_file_2)

    # Join dataframes
    try:
        final_dataframe = dataframe_first_file.join(
            dataframe_second_file.set_index(index_column_second_file),
            on=index_column_first_file,
            how=join_how_parameter,
        )

        final_dataframe = final_dataframe.drop_duplicates()

    except Exception as e:
        print(e)

    # Export csv file
    final_dataframe.to_csv(output, sep=delimiter, index=None)
    


# ================= MAIN =================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Join two csv datasets using columns as keys."
    )
    parser.add_argument("--first-file-path", type=str, required=True, help="File path of the first file")
    parser.add_argument(
        "--index-column-first-file",
        type=str,
        required=False,
        help="Name of the column of the first file. This will be use for merge datasets using index column as keys",
    )
    parser.add_argument("--second-file-path", type=str, required=True, help="File path of the second file")
    parser.add_argument(
        "--index-column-second-file",
        type=str,
        required=False,
        help="Name of the column of the second file. This will be use for merge datasets using index column as keys",
    )
    parser.add_argument(
        "--delimiter-file-1",
        type=str,
        required=False,
        help="Delimiter of the first file.",
    )
    parser.add_argument(
        "--delimiter-file-2",
        type=str,
        required=False,
        help="Delimiter of the second file.",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        help="Delimiter of the output file.",
    )
    parser.add_argument(
        "--join-how-parameter",
        type=str,
        required=False,
        help=f"How to handle the operation of the two objects."
        f"left (DEFAULT): use calling frame’s index (or column if on is specified.) "
        f"right: use other’s index. "
        f"outer: form union of calling frame’s index (or column if on is specified) with other’s index, and sort it. lexicographically."
        f"inner: form intersection of calling frame’s index (or column if on is specified) with other’s index, preserving the order of the calling’s one.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/output.csv",
        help="Output path.",
    )
    args = parser.parse_args()
   
    main(first_file_path = args.first_file_path,
    index_column_first_file = args.index_column_first_file,
    second_file_path = args.second_file_path,
    index_column_second_file = args.index_column_second_file,
    delimiter_file_1 = args.delimiter_file_1,
    delimiter_file_2 = args.delimiter_file_2,
    delimiter = args.delimiter,
    join_how_parameter = args.join_how_parameter, 
    output= args.output)
