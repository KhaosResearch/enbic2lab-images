import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd

from main import series_completion

input_data = pd.DataFrame(
    data={
        "DATE": ["1988-01-01", "1988-01-02", "1988-01-03", "1988-01-04", "1988-01-05"],
        "JABUGO": [20.5, 15.2, 30.1, 10.0, 25.5],
        "GALAROZA": [14.2, 12.3, 18.9, 9.7, 22.0],
        "CORTEGANA": [18.0, 10.6, 28.3, 11.8, 16.7],
        "ARACENA": [13.7, 11.8, 21.5, 8.9, 19.2],
        "ALAJAR": [19.1, 13.4, 27.8, 10.5, 23.0],
    }
)


def test_series_completion():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_output_file_comp_data = os.path.join(
            temp_dir, "output_completed_data_test.csv"
        )
        temp_output_file_analysis = os.path.join(temp_dir, "output_analysis_test.csv")
        temp_output_file_target = os.path.join(
            temp_dir, "output_target_completion_test.csv"
        )
        temp_output_file_tests = os.path.join(temp_dir, "output_tests_test.csv")

        pd.DataFrame(input_data).to_csv(temp_input_file, index=False, sep=delimiter)

        series_completion(
            filepath=temp_input_file,
            start_date="1988-01-01",
            end_date="1988-01-05",
            delimiter=delimiter,
            analysis_stations=["JABUGO", "GALAROZA", "CORTEGANA", "ARACENA", "ALAJAR"],
            target_station="JABUGO",
            completion_criteria=["r2"],
            output_completed_data=temp_output_file_comp_data,
            output_analysis=temp_output_file_analysis,
            output_target_completion=temp_output_file_target,
            output_tests=temp_output_file_tests,
        )

        assert os.path.exists(temp_output_file_comp_data)
        assert os.path.exists(temp_output_file_analysis)
        assert os.path.exists(temp_output_file_target)
        assert os.path.exists(temp_output_file_tests)

        assert os.path.getsize(temp_output_file_comp_data) > 0
        assert os.path.getsize(temp_output_file_analysis) > 0
        assert os.path.getsize(temp_output_file_target) > 0
        assert os.path.getsize(temp_output_file_tests) > 0

        assert pd.read_csv(temp_output_file_comp_data, sep=delimiter).shape == (0, 2)
        assert pd.read_csv(temp_output_file_analysis, sep=delimiter).shape == (4, 6)
        assert pd.read_csv(temp_output_file_target, sep=delimiter).shape == (5, 2)
        assert pd.read_csv(temp_output_file_tests, sep=delimiter).shape == (5, 4)
