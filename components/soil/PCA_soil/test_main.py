import os
from tempfile import TemporaryDirectory

import pytest
import pandas as pd
from filecmp import cmp

from main import pca_soil

input_CSV_data = pd.DataFrame(
    data={
        "pmm": [
            2.0118235236690243,
            2.0118235236690243,
            2.0118235236690243,
            2.0118235236690243,
            2.0118235236690243,
        ],
        "DensidadAp": [
            0.39138407455091107,
            0.10326717643267773,
            0.33559265208292927,
            0.6016427935533795,
            -0.29518350492447315,
        ],
        "Arenasmuyfinas": [
            -1.0470246316686154,
            -1.0470246316686154,
            -1.1925299358047003,
            -0.9717632674602947,
            -0.8613799332880911,
        ],
        "Textarenas": [
            -0.37551831269288166,
            -0.06809550027185787,
            -0.749410922394127,
            -1.1565384307354831,
            -0.4115227862196682,
        ],
        "Textlimos": [
            0.8891334268264451,
            0.07334736830271736,
            1.217767621018438,
            1.3994829989833828,
            0.9393951271146368,
        ],
        "Textarci": [
            -0.05511236739741996,
            0.6548035698028696,
            0.29984560120272485,
            1.0097615384030143,
            -0.05511236739741996,
        ],
        "ConductividadmSg": [
            1.2338318717498977,
            0.660770390845005,
            2.398440687782421,
            2.2875255624459907,
            2.740428990903083,
        ],
        "C.O.5cm": [
            0.30750429910142457,
            0.3451578596743032,
            0.8824013195031857,
            0.8033200652463938,
            0.9560408004370905,
        ],
        "M.O": [
            0.43688924382341154,
            0.48138101102735925,
            1.1161924493848554,
            1.0227493672152583,
            1.2032054859445576,
        ],
        "C.O.tha1": [
            0.6846322653384062,
            0.632385633770334,
            1.4558013560541159,
            1.472543575915479,
            1.236556820918539,
        ],
        "E.E": [
            -0.2124474892378325,
            -0.5629529560574339,
            1.3472762014744548,
            1.1704031313326146,
            -1.5332280836926802,
        ],
        "K.usle": [
            -0.36253510745995265,
            -0.7667297738124326,
            -0.8285308454265414,
            -0.7445057206537999,
            -0.8681311434665915,
        ],
        "CIC": [
            0.22044210701033307,
            0.22044210701033307,
            0.6671749004310659,
            0.8160858315713098,
            0.8160858315713098,
        ],
        "Ksat": [
            0.4759645565648454,
            1.6231038604342343,
            0.42838223403481374,
            1.941803083836664,
            1.7652065281311076,
        ],
        "nespecies": [
            1.149862488523563,
            1.149862488523563,
            1.149862488523563,
            1.149862488523563,
            1.149862488523563,
        ],
        "cobertura": [
            1.7570019557550207,
            1.7570019557550207,
            1.7570019557550207,
            1.7570019557550207,
            1.7570019557550207,
        ],
        "v1": [
            0.003583152880424975,
            0.33545349997287316,
            1.3679390242604892,
            1.3863762657656256,
            -0.07938443389268691,
        ],
        "v2": [
            -0.17292585195058843,
            0.3235398040112769,
            0.3235398040112769,
            -0.17292585195058843,
            -0.6693915079124535,
        ],
        "HumGen": [
            0.5144332706523439,
            1.056706188151153,
            2.234554863365477,
            0.8274363884733479,
            0.27041045777788003,
        ],
    }
)

expected_PCA_data_ncomp2 = pd.DataFrame(
    data={
        "PC1": [
            -0.8737201986502987,
            -1.1435042484378979,
            2.116629271498637,
            1.519587180198323,
            -1.6189920046087631,
        ],
        "PC2": [
            -0.8702901745109689,
            -1.278826097326873,
            -0.23752402665487585,
            0.6831016721048037,
            1.703538626387915,
        ],
    }
)

expected_PCA_data_var90 = pd.DataFrame(
    data={
        "PC1": [
            -0.8737201986502987,
            -1.1435042484378979,
            2.116629271498637,
            1.519587180198323,
            -1.6189920046087631,
        ],
        "PC2": [
            -0.8702901745109689,
            -1.278826097326873,
            -0.23752402665487585,
            0.6831016721048037,
            1.703538626387915,
        ],
        "PC3": [
            -0.6126357966787223,
            0.7169103463730357,
            -0.8243301287763948,
            1.0180030753000742,
            -0.2979474962179938,
        ],
    }
)


def test_pca_soil_ncomp2():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file_PCA = os.path.join(temp_dir, "expected_PCA.csv")
        temp_output_file_corrMatrix = os.path.join(
            temp_dir, "correlation_matrix_heatmap.csv"
        )
        temp_output_file_covMatrix = os.path.join(temp_dir, "covariance_matrix.csv")
        temp_output_file_PCA = os.path.join(temp_dir, "PCA_plot.csv")
        temp_output_file_scree = os.path.join(temp_dir, "scree_plot.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=";")
        expected_PCA_data_ncomp2.to_csv(temp_expected_file_PCA, index=False, sep=";")

        pca_soil(
            filepath=temp_input_file,
            number_components=2,
            delimiter=delimiter,
            output_corr_matrix=temp_output_file_corrMatrix,
            output_scree_plot=temp_output_file_scree,
            output_pca_plot=temp_output_file_PCA,
            output_cov_matrix=temp_output_file_covMatrix,
        )

        assert os.path.exists(temp_output_file_corrMatrix)
        assert os.path.exists(temp_output_file_covMatrix)
        assert os.path.exists(temp_output_file_PCA)
        assert os.path.exists(temp_output_file_scree)

        assert os.path.getsize(temp_output_file_corrMatrix) > 0
        assert os.path.getsize(temp_output_file_covMatrix) > 0
        assert os.path.getsize(temp_output_file_PCA) > 0
        assert os.path.getsize(temp_output_file_scree) > 0

        assert cmp(temp_output_file_PCA, temp_expected_file_PCA)


def test_pca_soil_var90():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file_PCA = os.path.join(temp_dir, "expected_PCA.csv")
        temp_output_file_corrMatrix = os.path.join(
            temp_dir, "correlation_matrix_heatmap.csv"
        )
        temp_output_file_covMatrix = os.path.join(temp_dir, "covariance_matrix.csv")
        temp_output_file_PCA = os.path.join(temp_dir, "PCA_plot.csv")
        temp_output_file_scree = os.path.join(temp_dir, "scree_plot.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=";")
        expected_PCA_data_var90.to_csv(temp_expected_file_PCA, index=False, sep=";")

        pca_soil(
            filepath=temp_input_file,
            variance_explained=90,
            delimiter=delimiter,
            output_corr_matrix=temp_output_file_corrMatrix,
            output_scree_plot=temp_output_file_scree,
            output_pca_plot=temp_output_file_PCA,
            output_cov_matrix=temp_output_file_covMatrix,
        )

        assert os.path.exists(temp_output_file_corrMatrix)
        assert os.path.exists(temp_output_file_covMatrix)
        assert os.path.exists(temp_output_file_PCA)
        assert os.path.exists(temp_output_file_scree)

        assert os.path.getsize(temp_output_file_corrMatrix) > 0
        assert os.path.getsize(temp_output_file_covMatrix) > 0
        assert os.path.getsize(temp_output_file_PCA) > 0
        assert os.path.getsize(temp_output_file_scree) > 0

        assert cmp(temp_output_file_PCA, temp_expected_file_PCA)


def test_pca_soil_var100():
    delimiter = ";"
    with TemporaryDirectory() as temp_dir:
        temp_input_file = os.path.join(temp_dir, "input_test.csv")
        temp_expected_file_PCA = os.path.join(temp_dir, "expected_PCA.csv")
        temp_output_file_corrMatrix = os.path.join(
            temp_dir, "correlation_matrix_heatmap.csv"
        )
        temp_output_file_covMatrix = os.path.join(temp_dir, "covariance_matrix.csv")
        temp_output_file_PCA = os.path.join(temp_dir, "PCA_plot.csv")
        temp_output_file_scree = os.path.join(temp_dir, "scree_plot.csv")

        input_CSV_data.to_csv(temp_input_file, index=False, sep=";")
        expected_PCA_data_var90.to_csv(temp_expected_file_PCA, index=False, sep=";")

        pca_soil(
            filepath=temp_input_file,
            variance_explained=100,
            delimiter=delimiter,
            output_corr_matrix=temp_output_file_corrMatrix,
            output_scree_plot=temp_output_file_scree,
            output_pca_plot=temp_output_file_PCA,
            output_cov_matrix=temp_output_file_covMatrix,
        )

        assert os.path.exists(temp_output_file_corrMatrix)
        assert os.path.exists(temp_output_file_covMatrix)
        assert os.path.exists(temp_output_file_PCA)
        assert os.path.exists(temp_output_file_scree)

        assert os.path.getsize(temp_output_file_corrMatrix) > 0
        assert os.path.getsize(temp_output_file_covMatrix) > 0
        assert os.path.getsize(temp_output_file_PCA) > 0
        assert os.path.getsize(temp_output_file_scree) > 0
