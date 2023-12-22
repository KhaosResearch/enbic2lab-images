from pathlib import Path
import os
import numpy as np
from numpy import savetxt, loadtxt
import argparse


def split_sequences_multivariable(filepath_features: str, filepath_target: str, n_steps_in: int, n_steps_out: int,
                                  delimiter: str, output_path: str):
    """
    Generates supervised data from a multidimensional array.

    Returns both data and its target for supervised learning (sequenceX.npy) (sequenceY.npy)
    """

    # Load array from CSV
    sequences_x = loadtxt(filepath_features, delimiter=delimiter)
    sequences_y = loadtxt(filepath_target, delimiter=delimiter)

    X, y = list(), list()
    for i in range(len(sequences_x)):
        # find the end of this pattern
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out - 1
        # check if we are beyond the dataset
        if out_end_ix > len(sequences_x):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences_x[i:end_ix, :], sequences_y[end_ix - 1: out_end_ix]
        X.append(seq_x)
        y.append(seq_y)

    X = np.array(X)
    y = np.array(y)

    # Save numpy arrays as binary (.npy) files
    sequence_x_path = Path(output_path, "sequenceX.npy")
    sequence_y_path = Path(output_path, "sequenceY.csv")

    np.save(sequence_x_path, X)
    np.save(sequence_y_path, y)


# ============ MAIN ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Multivarible sequence LSTM")
    parser.add_argument("--filepath-features", type=str, help="File path of the features csv file")
    parser.add_argument("--filepath-target", type=str, help="File path of the target csv file")
    parser.add_argument("--n-steps-in", type=int, default=12, help="Select time window to train the model")
    parser.add_argument("--n-steps-out", type=int, default=12, help="Select period of time to predict")
    parser.add_argument("--delimiter", type=str, default=";", help="Delimiter used in CSV.")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        help="Output path.",
    )
    args = parser.parse_args()

    split_sequences_multivariable(args.filepath_features, args.filepath_target,
                                  args.n_steps_in, args.n_steps_out, args.delimiter, args.output)
