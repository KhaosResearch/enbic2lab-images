import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd

from main import pca_heatmap

input_correlation_matrix_data = pd.DataFrame(
    data={
        "": [
            "pmm",
            "DensidadAp",
            "Arenasmuyfinas",
            "Textarenas",
            "Textlimos",
            "Textarci",
            "ConductividadmSg",
            "C.O.5cm",
            "M.O",
            "C.O.tha1",
            "E.E",
            "K.usle",
            "CIC",
            "Ksat",
            "nespecies",
            "cobertura",
            "v1",
            "v2",
            "HumGen",
        ],
        "pmm": [
            1.0,
            -0.44,
            -0.43,
            -0.46,
            0.35,
            0.45,
            0.56,
            0.8,
            0.82,
            0.82,
            0.39,
            -0.73,
            0.82,
            0.73,
            0.84,
            0.97,
            0.74,
            0.36,
            0.75,
        ],
        "DensidadAp": [
            -0.44,
            1.0,
            0.34,
            0.48,
            -0.38,
            -0.15,
            -0.59,
            -0.62,
            -0.64,
            -0.43,
            -0.24,
            0.47,
            -0.46,
            -0.41,
            -0.43,
            -0.49,
            -0.38,
            -0.11,
            -0.34,
        ],
        "Arenasmuyfinas": [
            -0.43,
            0.34,
            1.0,
            0.41,
            -0.25,
            -0.16,
            -0.43,
            -0.45,
            -0.47,
            -0.44,
            -0.15,
            0.7,
            -0.42,
            -0.34,
            -0.38,
            -0.45,
            -0.36,
            -0.2,
            -0.34,
        ],
        "Textarenas": [
            -0.46,
            0.48,
            0.41,
            1.0,
            -0.73,
            -0.48,
            -0.61,
            -0.52,
            -0.54,
            -0.47,
            -0.27,
            0.33,
            -0.5,
            -0.37,
            -0.58,
            -0.47,
            -0.41,
            -0.19,
            -0.35,
        ],
        "Textlimos": [
            0.35,
            -0.38,
            -0.25,
            -0.73,
            1.0,
            0.17,
            0.47,
            0.44,
            0.44,
            0.37,
            0.1,
            -0.04,
            0.35,
            0.28,
            0.27,
            0.28,
            0.19,
            0.01,
            0.16,
        ],
        "Textarci": [
            0.45,
            -0.15,
            -0.16,
            -0.48,
            0.17,
            1.0,
            0.07,
            0.32,
            0.35,
            0.34,
            0.27,
            -0.43,
            0.49,
            0.31,
            0.57,
            0.43,
            0.41,
            0.23,
            0.42,
        ],
        "ConductividadmSg": [
            0.56,
            -0.59,
            -0.43,
            -0.61,
            0.47,
            0.07,
            1.0,
            0.68,
            0.69,
            0.61,
            0.32,
            -0.5,
            0.5,
            0.5,
            0.47,
            0.57,
            0.35,
            0.1,
            0.3,
        ],
        "C.O.5cm": [
            0.8,
            -0.62,
            -0.45,
            -0.52,
            0.44,
            0.32,
            0.68,
            1.0,
            0.97,
            0.95,
            0.36,
            -0.78,
            0.74,
            0.62,
            0.66,
            0.79,
            0.58,
            0.26,
            0.58,
        ],
        "M.O": [
            0.82,
            -0.64,
            -0.47,
            -0.54,
            0.44,
            0.35,
            0.69,
            0.97,
            1.0,
            0.94,
            0.36,
            -0.8,
            0.76,
            0.62,
            0.69,
            0.81,
            0.61,
            0.27,
            0.61,
        ],
        "C.O.tha1": [
            0.82,
            -0.43,
            -0.44,
            -0.47,
            0.37,
            0.34,
            0.61,
            0.95,
            0.94,
            1.0,
            0.35,
            -0.78,
            0.72,
            0.61,
            0.68,
            0.8,
            0.6,
            0.29,
            0.6,
        ],
        "E.E": [
            0.39,
            -0.24,
            -0.15,
            -0.27,
            0.1,
            0.27,
            0.32,
            0.36,
            0.36,
            0.35,
            1.0,
            -0.36,
            0.39,
            0.26,
            0.45,
            0.41,
            0.29,
            0.11,
            0.28,
        ],
        "K.usle": [
            -0.73,
            0.47,
            0.7,
            0.33,
            -0.04,
            -0.43,
            -0.5,
            -0.78,
            -0.8,
            -0.78,
            -0.36,
            1.0,
            -0.68,
            -0.53,
            -0.66,
            -0.75,
            -0.58,
            -0.29,
            -0.58,
        ],
        "CIC": [
            0.82,
            -0.46,
            -0.42,
            -0.5,
            0.35,
            0.49,
            0.5,
            0.74,
            0.76,
            0.72,
            0.39,
            -0.68,
            1.0,
            0.62,
            0.74,
            0.81,
            0.62,
            0.3,
            0.63,
        ],
        "Ksat": [
            0.73,
            -0.41,
            -0.34,
            -0.37,
            0.28,
            0.31,
            0.5,
            0.62,
            0.62,
            0.61,
            0.26,
            -0.53,
            0.62,
            1.0,
            0.61,
            0.7,
            0.57,
            0.33,
            0.59,
        ],
        "nespecies": [
            0.84,
            -0.43,
            -0.38,
            -0.58,
            0.27,
            0.57,
            0.47,
            0.66,
            0.69,
            0.68,
            0.45,
            -0.66,
            0.74,
            0.61,
            1.0,
            0.87,
            0.79,
            0.39,
            0.76,
        ],
        "cobertura": [
            0.97,
            -0.49,
            -0.45,
            -0.47,
            0.28,
            0.43,
            0.57,
            0.79,
            0.81,
            0.8,
            0.41,
            -0.75,
            0.81,
            0.7,
            0.87,
            1.0,
            0.74,
            0.34,
            0.75,
        ],
        "v1": [
            0.74,
            -0.38,
            -0.36,
            -0.41,
            0.19,
            0.41,
            0.35,
            0.58,
            0.61,
            0.6,
            0.29,
            -0.58,
            0.62,
            0.57,
            0.79,
            0.74,
            1.0,
            0.56,
            0.93,
        ],
        "v2": [
            0.36,
            -0.11,
            -0.2,
            -0.19,
            0.01,
            0.23,
            0.1,
            0.26,
            0.27,
            0.29,
            0.11,
            -0.29,
            0.3,
            0.33,
            0.39,
            0.34,
            0.56,
            1.0,
            0.57,
        ],
        "HumGen": [
            0.75,
            -0.34,
            -0.34,
            -0.35,
            0.16,
            0.42,
            0.3,
            0.58,
            0.61,
            0.6,
            0.28,
            -0.58,
            0.63,
            0.59,
            0.76,
            0.75,
            0.93,
            0.57,
            1.0,
        ],
    }
)


def test_pca_heatmap():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file = os.path.join(temp_dir, "output_plot.pdf")

        input_correlation_matrix_data.to_csv(temp_input_file, index=False, sep=";")

        pca_heatmap(
            filepath=temp_input_file,
            delimiter=delimiter,
            output=temp_output_file,
        )

        assert os.path.isfile(temp_output_file)
        assert os.path.getsize(temp_output_file) > 0
