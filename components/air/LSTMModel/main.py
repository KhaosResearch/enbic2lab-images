import os
from pathlib import Path
from typing import Tuple
import argparse
import keras
import keras.metrics as metric
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.layers import (
    LSTM,
    Conv1D,
    Dense,
    Flatten,
    MaxPooling1D,
    RepeatVector,
    TimeDistributed,
)
from keras.models import Sequential
from numpy import load, loadtxt, ndarray, save

def split_train_test(X: ndarray, y: ndarray, n_steps_out) -> Tuple[ndarray, ndarray, ndarray, ndarray]:

    X_train = X[:-n_steps_out, :, :]
    y_train = y[:-n_steps_out, :]
    X_test = X[-n_steps_out:, :, :]
    y_test = y[-n_steps_out:, :]

    return X_train, y_train, X_test, y_test


def train_model(
    X_train: ndarray,
    y_train: ndarray,
    X_test: ndarray,
    y_test: ndarray,
    model: Sequential,
    saved_model: str,
) -> Sequential:

    checkpointer = ModelCheckpoint(filepath=saved_model, verbose=1, save_best_only=True)

    early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=20, restore_best_weights=True)
    sch = ReduceLROnPlateau(monitor="val_loss", factor=0.01, patience=5, min_lr=1e-8, verbose=1)

    model.fit(
        X_train,
        y_train,
        epochs=1000,
        validation_data=(X_test, y_test),
        callbacks=[checkpointer, sch, early_stop],
    )

    return model
def main(filepath_X: str,filepath_Y: str,output:str,   n_steps_in : int , n_steps_out :int,delimiter: str = ";", n_neurons : int = 200):
    """
    Given some parameters, builds a ConvLSTM model for timeseries analysis.

    Returns the built Keras model and X_test, y_test to make predictions
    """
    
    # Load array
    X = load(filepath_X)
    y = loadtxt(filepath_Y, delimiter=delimiter)

    # Split train and test
    X_train, y_train, X_test, y_test = split_train_test(X, y, n_steps_out)

    # extract the number of features
    n_features = X_train.shape[2]

    # Build LSTM MODEL
    model = Sequential()
    model.add(
        Conv1D(
            filters=64,
            kernel_size=3,
            activation="relu",
            input_shape=(n_steps_in, n_features),
        )
    )
    model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())

    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(n_neurons, activation="relu", return_sequences=True))
    model.add(TimeDistributed(Dense(n_neurons, activation="relu")))
    model.add(TimeDistributed(Dense(1)))

    model.compile(loss="mse", optimizer="adam", metrics=[metric.RootMeanSquaredError()])
    model.summary()

    # Train and Save the model
    saved_model = output + "lstm_model.h5"
    train_model(X_train, y_train, X_test, y_test, model, saved_model)

    # Save numpy array
    filename = "lstm" + "_X_test"
    filename_target = "lstm" + "_Y_test"
    path_x_test = Path(output, filename)
    path_y_test = Path(output, filename_target)

    save(path_x_test, X_test)
    save(path_y_test, y_test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sarima model")

    # Define command-line arguments
    parser.add_argument(
        "--filepath-X",
        type=str,
        default="/mnt/shared/sequences_X.npy",
        required=True,
        help="Path to the input NPY file with the data needed to build the corresponding graph",
    )
    parser.add_argument(
        "--filepath-Y",
        type=str,
        default="/mnt/shared/sequences_Y.csv",
        required=True,
        help="Path to the input CSV file with the data needed to build the corresponding graph",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--n-neurons",
        type=int,
        default=200,
        required=True,
        help="Set the seasonality of your pollen",
    )
    parser.add_argument(
        "--n-steps-in",
        type=int,
        required=True,
        help="Set the seasonality of your pollen",
    )
    parser.add_argument(
        "--n-steps-out",
        type=int,
        required=True,
        help="Set the seasonality of your pollen",
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        required=True,
        help="Path to the output where files are saved",
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath_X,
        args.filepath_Y,
        args.output,
        args.n_steps_in,
        args.n_steps_out,
        args.delimiter,
        args.n_neurons,
    )
