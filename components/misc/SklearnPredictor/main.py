import onnxruntime as rt
import pandas as pd
import numpy as np

from argparse import ArgumentParser

def sklearn_predictor(
    filepath_model: str,
    filepath_data: str,
    output: str,
    delimiter: str = ";",
):
    sess = rt.InferenceSession(filepath_model, providers=["CPUExecutionProvider"])
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name

    data_to_predict = pd.read_csv(filepath_data, sep=delimiter, decimal=".", header=0)

    match sess.get_inputs()[0].type:
        case "tensor(double)":
            X = data_to_predict.to_numpy(dtype=np.float64)
        case "tensor(float)":
            X = data_to_predict.to_numpy(dtype=np.float32)
        case "tensor(float16)":
            X = data_to_predict.to_numpy(dtype=np.float16)
        case "tensor(int8)":
            X = data_to_predict.to_numpy(dtype=np.int8)
        case "tensor(int16)":
            X = data_to_predict.to_numpy(dtype=np.int16)
        case "tensor(int32)":
            X = data_to_predict.to_numpy(dtype=np.int32)
        case "tensor(int64)":
            X = data_to_predict.to_numpy(dtype=np.int64)
        case _:  # type: ignore
            X = data_to_predict.to_numpy()

    pred_onx = sess.run([label_name], {input_name: X})[0]

    df_predicted = pd.concat([data_to_predict, pd.DataFrame(pred_onx, columns=["prediction"])], axis=1)

    df_predicted.to_csv(f"{output}/predictions.csv", index=False)

if __name__ == "__main__":
    parser = ArgumentParser(description="Sklearn Predictor")
    parser.add_argument(
        "--filepath-model",
        type=str,
        required=True,
        help="File path to the model",
        dest="filepath_model",
        metavar="STRING",
    )
    parser.add_argument(
        "--filepath-data",
        type=str,
        required=True,
        help="File path to the CSV prediction set",
        dest="filepath_data",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter of the CSV prediction set",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path for the results",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    sklearn_predictor(
        filepath_model=args.filepath_model,
        filepath_data=args.filepath_data,
        delimiter=args.delimiter,
        output=args.output,
    )