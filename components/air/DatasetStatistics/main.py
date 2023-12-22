from re import findall
import numpy as np
import pandas as pd
import argparse


def main(
    filepath: str,
    output: str,
    delimiter: str = ";",
    acum_list_attr: str = ["sol,prec,Hum_rel"],
    mm_list_attr: str = ["tmed,tmax,tmin,dir,velmedia,racha,sol,presMax,presMin,Index,prec,CALMA,Hum_rel,Vto_1,Vto_2,Vto_3,Vto_4"],
):
    """
    This Python component calculates evapotranspiration using an input CSV file containing necessary data for the calculation.

    Args:
        filepath (str) --> File path of the CSV File.
        acum_list_attr (List[str]) --> List of attributes for doing statistics with them.
        mm_list_attr (List[str]) --> List of attributes for mm statistic.
        delimiter (str) --> Delimiter of the CSV File.
        outfile_name (str) --> Name of the output CSV file.
    """
    df = pd.read_csv(filepath, sep=';', decimal=',')
    dict_statistic = {}
    for att in acum_list_attr:
        if att in df.columns.tolist() and att in acum_list_attr:
            dict_statistic[att+"_acum_3"] = [np.nan,np.nan,np.nan]
            dict_statistic[att+"_acum_5"] = [np.nan,np.nan,np.nan,np.nan,np.nan]
            for i in range(3, df.shape[0]):
                dict_statistic[att+"_acum_3"].insert(i, round(float(df[att][i-1])+float(df[att][i-2])+float(df[att][i-3]),3))
            for i in range(5, df.shape[0]):
                dict_statistic[att+"_acum_5"].insert(i, round(float(df[att][i-1])+float(df[att][i-2])+float(df[att][i-3])+float(df[att][i-4])+float(df[att][i-5]),3))
    for att in mm_list_attr:
        if att in df.columns.tolist() and att in mm_list_attr:
            dict_statistic[att+"_mm_3"] = [np.nan,np.nan,np.nan]
            dict_statistic[att+"_mm_5"] = [np.nan,np.nan,np.nan,np.nan,np.nan]
            for i in range(3, df.shape[0]):
                dict_statistic[att+"_mm_3"].insert(i, round((float(df[att][i-1])+float(df[att][i-2])+float(df[att][i-3]))/3,3))
            for i in range(5, df.shape[0]):
                dict_statistic[att+"_mm_5"].insert(i, round((float(df[att][i-1])+float(df[att][i-2])+float(df[att][i-3])+float(df[att][i-4])+float(df[att][i-5]))/5,3))
    # Crear DataFrame auxiliar a partir de dict_statistic
    df_statistic = pd.DataFrame(dict_statistic)
    # Concatenar el DataFrame original con el DataFrame auxiliar
    df = pd.concat([df, df_statistic], axis=1)
    # Exportar a CSV
    df.to_csv(output, sep=delimiter, index=False)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistics component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath", type=str, required=True, help="Path to the input CSV File"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--acum-list-attr",
        type=str,
        default="sol,prec,Hum_rel",
        required=True,
        help="List of attributes for doing statistics with them.",
    )
    parser.add_argument(
        "--mm-list-attr",
        type=str,
        default="tmed,tmax,tmin,dir,velmedia,racha,sol,presMax,presMin,Index,prec,CALMA,Hum_rel,Vto_1,Vto_2,Vto_3,Vto_4",
        required=False,
        help="List of attributes for mm statistic.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help=" Name of the output CSV file.",
    )

    args = parser.parse_args()
    args.acum_list_attr = findall(r'\s*([^,]+)\s*', args.acum_list_attr) if args.acum_list_attr != None else None
    args.mm_list_attr = findall(r'\s*([^,]+)\s*', args.mm_list_attr) if args.mm_list_attr != None else None


    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.output,
        args.delimiter,
        args.acum_list_attr,
        args.mm_list_attr,
    )
