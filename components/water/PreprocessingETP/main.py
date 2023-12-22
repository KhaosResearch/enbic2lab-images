import argparse

import numpy as np
import pandas as pd


def calcular_metricas(data, cte1, cte2, kt):
    new_dict = {}
    new_dict["Fecha"] = data["Fecha"].dt.strftime("%d/%m/%Y")
    new_dict["TMedia"] = (data["TMAX"] + data["TMIN"]) / 2

    julian_day = data["Fecha"].dt.dayofyear
    new_dict["Día juliano"] = julian_day
    new_dict["Distancia Tierra-Sol"] = 1 + 0.033 * np.cos(
        (2 * np.pi) * julian_day / 365
    )
    new_dict["Declinación diaria en grados"] = 23.45 * np.sin(
        2 * np.pi * (julian_day + 284) / 365
    )
    new_dict["Latitud RAD"] = np.radians(data["Latitud"])
    new_dict["Declinación RAD"] = np.radians(new_dict["Declinación diaria en grados"])
    new_dict["(menos)Tangente"] = -np.tan(new_dict["Latitud RAD"])
    new_dict["Tangente declinación"] = np.tan(new_dict["Declinación RAD"])
    new_dict["Multiplicación"] = (
        new_dict["(menos)Tangente"] * new_dict["Tangente declinación"]
    )
    new_dict["Angulo horario (radianes)"] = np.arccos(new_dict["Multiplicación"])
    new_dict["Angulo horario (Grados)"] = np.degrees(
        new_dict["Angulo horario (radianes)"]
    )
    new_dict["CTE1"] = float(cte1)
    new_dict["CTE2"] = float(cte2)
    new_dict["Seno latitud"] = np.sin(new_dict["Latitud RAD"])
    new_dict["Seno declinación"] = np.sin(new_dict["Declinación RAD"])
    new_dict["Coseno latitud"] = np.cos(new_dict["Latitud RAD"])
    new_dict["Coseno declinación"] = np.cos(new_dict["Declinación RAD"])
    new_dict["Seno ángulo horario"] = np.sin(new_dict["Angulo horario (radianes)"])
    new_dict["tmax-tmin^0,5"] = (data["TMAX"] - data["TMIN"]) ** 0.5
    new_dict["tmax-tmin^0,99"] = (data["TMAX"] - data["TMIN"]) ** 0.99
    new_dict["tmax-tmin^0,75"] = (data["TMAX"] - data["TMIN"]) ** 0.75
    new_dict["tmax-tmin^0,25"] = (data["TMAX"] - data["TMIN"]) ** 0.25
    new_dict["tmax-tmin^0,01"] = (data["TMAX"] - data["TMIN"]) ** 0.01
    new_dict["KT"] = float(kt)
    new_dict["Ro"] = (
        float(cte1)
        * new_dict["Distancia Tierra-Sol"]
        * (
            float(cte2)
            * new_dict["Angulo horario (Grados)"]
            * new_dict["Seno latitud"]
            * new_dict["Seno declinación"]
            + new_dict["Coseno latitud"]
            * new_dict["Coseno declinación"]
            * new_dict["Seno ángulo horario"]
        )
    )
    new_dict["Ro EXTRATERRESTRE mm/dia"] = new_dict["Ro"] * 0.408
    new_dict["Rs"] = (
        new_dict["Ro EXTRATERRESTRE mm/dia"] * float(kt) * new_dict["tmax-tmin^0,5"]
    )
    new_dict["Ravanazzi"] = (
        (0.817 + 0.00022 * 625)
        * 0.0023
        * new_dict["Ro EXTRATERRESTRE mm/dia"]
        * (new_dict["TMedia"] + 17.78)
        * new_dict["tmax-tmin^0,5"]
    )

    df = pd.DataFrame(new_dict)

    return df


def main(filepath: str, cte1: str, cte2: str, kt: str, output: str):
    data = pd.read_excel(filepath)

    df_final = calcular_metricas(data, cte1=cte1, cte2=cte2, kt=kt)
    data_without_date = data.drop("Fecha", axis=1)
    df_final = pd.concat([data_without_date, df_final], axis=1)

    df_final.to_csv(output, index=False, sep=";")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=".")
    parser.add_argument(
        "--filepath", type=str, required=True, help="Path of ETP file."
    )
    parser.add_argument("--cte1", type=str, required=True, help="CTE1")
    parser.add_argument("--cte2", type=str, required=True, help="CTE2")
    parser.add_argument("--kt", type=str, required=True, help="KT")
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/",
        help="Output path."
    )
    args = parser.parse_args()

    main(
        args.filepath,
        args.cte1,
        args.cte2,
        args.kt,
        args.output + "ETP_preprocessing.csv",
    )
