import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

from main import homogeneity_plot

# Define test data and file paths
test_data_1 = pd.DataFrame(
    data={
        "DATE": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04", "2019-01-05", "2019-01-06", "2019-01-07", "2019-01-08", "2019-01-09", "2019-01-10"],
        "STATION1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
)

test_data_2 = pd.DataFrame(
    data = {
        '': ['Homogeneity', 'Change Point Location', 'P-value', 'Maximum test Statistics', 'Average between change point'],
        'Pettit Test': [True, '1995-10-11', 0.0844, 1665798.0, 'mean(mu1=2.997601944966295, mu2=3.2553188511849784)'],
        'SNHT Test': [True, '1971-06-05', 0.0741, 10.744027767906422, 'mean(mu1=5.813548387096774, mu2=3.097732604437119)'],
        'Buishand Test': [True, '2003-04-23', 0.0006, 2.4152090527890273, 'mean(mu1=3.2982033898305088, mu2=2.7547689675182907)']
    }
)


def test_homogeneity_plot():
    delimiter = ";"

    with TemporaryDirectory() as tmp_dir:
        tmp_input_file_precipitations = os.path.join(
            tmp_dir, "test_input_precipitations.csv"
        )
        tmp_input_file_homogen = os.path.join(tmp_dir, "test_input_homogen.csv")
        tmp_output_file = os.path.join(tmp_dir, "test_output.html")

        test_data_1.to_csv(
            tmp_input_file_precipitations, sep=delimiter, decimal=".", index=False
        )
        test_data_2.to_csv(
            tmp_input_file_homogen, sep=delimiter, decimal=".", index=False
        )

        homogeneity_plot(
            filepath_data=tmp_input_file_precipitations,
            filepath_homogeneity=tmp_input_file_homogen,
            data_type="precipitation",
            criteria="Pettit Test",
            output=tmp_output_file,
            delimiter=delimiter,
        )

        # Check if the output file exists
        assert os.path.exists(tmp_output_file)
        assert os.path.isfile(tmp_output_file)
        assert os.path.getsize(tmp_output_file) > 0


if __name__ == "__main__":
    pytest.main()
