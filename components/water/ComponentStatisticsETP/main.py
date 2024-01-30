import ast
import typer
import numpy as np
import pandas as pd
from scipy import stats
from re import findall
import argparse

def main(
    filepath: str,
    output_filepath: str,
    start_year: int,
    end_year: int,
    variables_list: str,
    metrics_list: str,
    hydrological_year: str = "False",
    delimiter: str = ";",
) -> None:
    df = pd.read_table(filepath, delimiter=delimiter)
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")
    df_metrics = pd.DataFrame()
    
    hydrological_year = ast.literal_eval(hydrological_year)

    if hydrological_year:
        start_date, end_date = f"{start_year}-10-1", f"{end_year}-09-30"

    else:
        start_date, end_date = f"{start_year}-01-01", f"{end_year}-12-31"

    dates = (df["Fecha"] >= start_date) & (df["Fecha"] <= end_date)
    df_per_year = df.loc[dates]

    for variable in variables_list:
        if "ETP" in variable:
            variable = "ETP"
            df_per_year = df_per_year.rename(
                columns={
                    col: "ETP" for col in df_per_year.columns if col.startswith("ETP")
                }
            )
        if variable in df_per_year.columns:
            for metric in metrics_list:
                if metric == "Mean":
                    df_metrics[f"{variable}_{metric}"] = [df_per_year[variable].mean()]
                elif metric == "Median":
                    df_metrics[f"{variable}_{metric}"] = [np.median(df_per_year[variable])]
                elif metric == "Min":
                    df_metrics[f"{variable}_{metric}"] = [df_per_year[variable].min()]
                elif metric == "Max":
                    df_metrics[f"{variable}_{metric}"] = [df_per_year[variable].max()]
                elif metric == "Range":
                    df_metrics[f"{variable}_{metric}"] = [
                        df_per_year[variable].max() - df_per_year[variable].min()
                    ]
                elif metric == "Variance":
                    df_metrics[f"{variable}_{metric}"] = [np.var(df_per_year[variable])]
                elif metric == "Standard-Deviation":
                    df_metrics[f"{variable}_{metric}"] = [np.std(df_per_year[variable])]
                elif metric == "Variation-Coefficient":
                    df_metrics[f"{variable}_{metric}"] = [stats.variation(df_per_year[variable])]
                elif metric == "Asymmetry-Coefficient":
                    df_metrics[f"{variable}_{metric}"] = [
                        stats.skew(df_per_year[variable], axis=0, bias=True)
                    ]
                elif metric == "Kurtosis":
                    df_metrics[f"{variable}_{metric}"] = [
                        stats.kurtosis(df_per_year[variable], axis=0, fisher=True, bias=True)
                    ]
                else:
                    typer.echo(
                        "Unknown metrics. Valid metrics: Mean, Median, Min, Max, Range, Variance, "
                        "Standard Deviation, Variation Coefficient, Asymmetry Coefficient, Kurtosis"
                    )
                    raise typer.Abort()
        else:
            typer.echo(
                "Unknown variable name. Introduce the variable as it is in the CSV entered and with no spaces between them"
            )
            raise typer.Abort()
    print(output_filepath)
    df_final = df_metrics.transpose()
    df_final.to_csv(
        output_filepath, index=True, header=False, decimal=".", sep=delimiter
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP statistics component")
    parser.add_argument(
        "--filepath", type=str, required=True, help="Path to the input CSV File"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=True,
        default=";",
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--start-year", type=int, required=True, help="Start Date to calculate metrics"
    )
    parser.add_argument(
        "--end-year", type=int, required=True, help="End Date to calculate metrics"
    )
    parser.add_argument(
        "--variables-list",
        type=str,
        required=True,
        help="A list of the variables to calculate its metrics.",
    )
    parser.add_argument(
        "--metrics-list", type=str, required=True, help="A list of the metrics."
    )
    parser.add_argument(
        "--hydrological-year",
        type=str,
        required=True,
        default="False",
        help="String to choose whether the representation is by hydrological year or not",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
    )
    args = parser.parse_args()
    args.variables_list = findall(r'\s*([^,]+)\s*', args.variables_list) if args.variables_list != None else None
    args.metrics_list = findall(r'\s*([^,]+)\s*', args.metrics_list) if args.metrics_list != None else None

    main(
        args.filepath,
        args.output,
        args.start_year,
        args.end_year,
        args.variables_list,
        args.metrics_list,
        args.hydrological_year,
        args.delimiter,
    )
