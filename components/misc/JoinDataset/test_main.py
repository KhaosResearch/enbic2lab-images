import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd

from main import main, createDataFrame


@pytest.fixture
def sample_data():
    # Datos de muestra para pruebas
    data_first_file = "Fecha,TMAX,TMIN\n01/10/2003,20.9,16.5\n02/10/2003,19.5,15.7"
    data_second_file = "Fecha,Precipitación\n01/10/2003,6.2\n02/10/2003,16.6"

    return data_first_file, data_second_file


def test_main(sample_data, tmp_path):
    # Prueba para la función main
    data_first_file, data_second_file = sample_data
    file_first_path = tmp_path / "first_file.csv"
    file_second_path = tmp_path / "second_file.csv"
    output_path = tmp_path / "output.csv"

    # Guardar datos de muestra en archivos temporales
    file_first_path.write_text(data_first_file)
    file_second_path.write_text(data_second_file)

    # Ejecutar la función main con los archivos temporales
    main(
        first_file_path=str(file_first_path),
        index_column_first_file="Fecha",
        second_file_path=str(file_second_path),
        index_column_second_file="Fecha",
        delimiter_file_1=",",
        delimiter_file_2=",",
        delimiter=",",
        join_how_parameter="left",
        output=str(output_path),
    )

    # Verificar que el archivo de salida se haya creado
    assert output_path.exists()

    # Leer el archivo de salida y verificar su contenido
    result_df = pd.read_csv(output_path)
    expected_result = pd.DataFrame({
        "Fecha": ["01/10/2003", "02/10/2003"],
        "TMAX": [20.9, 19.5],
        "TMIN": [16.5, 15.7],
        "Precipitación": [6.2, 16.6]
    })

    assert result_df.equals(expected_result)