from time import time
import argparse
import warnings
import os
import itertools
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import pyplot
import matplotlib.dates as mdates

plt.style.use("fivethirtyeight")
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.api as sma
from pylab import rcParams
from sklearn.metrics import mean_squared_error
from scipy.signal import find_peaks

warnings.filterwarnings("ignore")
matplotlib.rcParams["axes.labelsize"] = 20
matplotlib.rcParams["xtick.labelsize"] = 20
matplotlib.rcParams["ytick.labelsize"] = 20
matplotlib.rcParams["text.color"] = "k"
matplotlib.rcParams['axes.facecolor'] = 'white'


def test_stationary(timeseries, output_path):
    # Determine rolling statistics
    rol_mean = timeseries.rolling(window=12, center=True).mean()
    rol_std = timeseries.rolling(window=12, center=True).std()
    # rolling statistics plot
    pyplot.figure(figsize=(40, 20))
    ax = plt.gca()
    ### formatter of the date
    ax.xaxis.set_major_locator(mdates.YearLocator())
    plt.xlabel("Date", fontsize=50)
    plt.ylabel("Count", labelpad=5, fontsize=50)
    plt.plot(timeseries, color="black", label='Time Series')
    plt.plot(rol_mean, color="red", label='Mean rolling')
    plt.plot(rol_std, color="blue", label='Std. rolling')
    plt.legend(loc="best", prop={"size": 10})
    ax.patch.set_alpha(0.0)
    # plt.title("Time series with rolling mean and std")
    plt.savefig(output_path + "DickeyFuller_plot.png")
    # Dickey-Fuller test
    test_dataframe = pd.DataFrame()
    dftest = adfuller(timeseries.values, autolag="AIC")
    stat = dftest[0]
    test_dataframe.loc["Test statistic", "value"] = stat
    p_value = dftest[1]
    test_dataframe.loc["p-value", "value"] = p_value
    c_values = dftest[4]
    for c_level in [10, 5, 1]:
        conf = 100 - c_level
        cval = c_values["%i%%" % c_level]
        if stat < cval:
            comp = ">"
            verdict = "Pass"
        else:
            comp = "<"
            verdict = "Fails"

        test_dataframe.loc["Confidence " + str(conf) + " %", "value"] = (
                str(cval) + " " + str(comp) + " " + str(stat) + " ... " + str(verdict)
        )

    return test_dataframe


def decompose_and_analyze(data, year, dickey_fuller, output_path):
    rcParams["figure.figsize"] = 18, 8
    pyplot.figure(figsize=(150, 120))
    data.index = pd.DatetimeIndex(data.index)
    decomposition = sm.tsa.seasonal_decompose(data, model="additive")
    fig = decomposition.seasonal.iloc[-14:-2].plot(linewidth=30, color="black")
    plt.ylabel("Seasonality")
    plt.xlabel("Date")
    fig.patch.set_alpha(0.0)
    plt.savefig(output_path + "seasonality.pdf")

    dates = pd.Series(
        pd.to_datetime(decomposition.seasonal.index), index=decomposition.seasonal.index
    )
    dates_filter = dates[dates.dt.year == int(year)]
    seasonal_dataframe = pd.DataFrame(decomposition.seasonal.loc[dates_filter])
    seasonal_dataframe.seasonal = seasonal_dataframe.seasonal.astype(int)
    picks = find_peaks(seasonal_dataframe.seasonal)

    end_df = dickey_fuller
    if len(picks[0]) == 1:
        end_df.loc["Seasonal", "value"] = True
    else:
        end_df.loc["Seasonal", "value"] = False

    end_df.to_csv(output_path + "DickerFuller_seasonality.csv", sep=";")


def find_best_arima_model(data):
    p = q = range(0, 3)
    d = D = range(0, 1)
    P = Q = range(0, 3)

    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(P, D, Q))]

    min_aic = float('inf')
    best_model = None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(
                    data,
                    order=param,
                    seasonal_order=param_seasonal,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                )
                results = mod.fit(disp=False)
                if results.aic < min_aic:
                    min_aic = results.aic
                    best_model = mod

            except Exception as e:
                continue
    return best_model


def plot_arima_diagnostics(model, output_path):
    results = model.fit(disp=False)
    results.plot_diagnostics(lags=12,figsize=(16, 8))
    plt.tight_layout()
    plt.savefig(output_path, format="pdf")


def arima_analysis(data, output_path):
    """
    Perform Seasonality model selection and diagnostics analysis.

    Parameters:
    - data (pd.Series): Time series data.
    - output_path (str): Output path for saving diagnostic plots.
    """
    best_model = find_best_arima_model(data)

    if best_model is not None:
        plot_path = output_path + "SARIMAX_plots.pdf"
        plot_arima_diagnostics(best_model, plot_path)
    else:
        print("Failed to find a suitable SARIMAX model.")


def main(filepath: str, delimiter: str, date_column: str, pollen: str, year: int, output_path: str):
    dataframe = pd.read_csv(filepath, sep=delimiter)

    df = pd.DataFrame()
    df[date_column] = dataframe[date_column]
    df[pollen] = dataframe[pollen]
    df[date_column] = pd.to_datetime(df[date_column]).dt.strftime("%m-%Y")

    dates = df[date_column].unique()
    data = pd.DataFrame()
    data[date_column] = dates
    data = data.set_index(date_column)

    for date in dates:
        data.loc[date, pollen] = df.loc[df[date_column] == date, pollen].sum()

    # test de dickey-fuller
    dickey_fuller = test_stationary(data[pollen], output_path)

    # Descompone la serie temporal y observa la estacionaridad y estacionalidad
    decompose_and_analyze(data, year, dickey_fuller, output_path)

    # Genera y guarda los gráficos de diagnóstico del modelo SARIMAX.
    arima_analysis(data, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the altitude range of each community.")
    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the csv file",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        help="Delimiter of the input file and output file",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default="fecha",
        help="Date column in pollen dataset",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--pollen-column",
        type=str,
        help="Name of the Pollen column",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Year for decomposition",
        required=True,
        metavar="INTEGER"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared/",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()
    main(filepath=args.filepath,
         delimiter=args.delimiter,
         date_column=args.date_column,
         pollen=args.pollen_column,
         year=args.year,
         output_path=args.output)
