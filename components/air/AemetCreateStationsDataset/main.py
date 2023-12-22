import csv
import pandas as pd
import json
import numpy as np
import argparse

def main(
    filepath: str,
    output: str,
    attribute: str = "prec",
    delimiter: str = ";"    
):
    """
    Create a CSV File with data about an attribute from Aemet for differents stations

    Args:
        filepath (str) --> File path of the CSV File.
        attribute (str) -->  Selected attribute of the dataset.
        delimiter (str) --> Delimiter of the CSV File.
        output (str) --> Filepath of the output CSV file.
    """
   # Cargar el JSON desde el archivo
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)

    # Crear un diccionario para almacenar los valores de cada indicativo
    indicativos_data = {}

    # Procesar cada entrada en el JSON
    # Procesar cada entrada en el JSON
    for entry in data:
        fecha = entry['fecha']
        indicativo = entry['indicativo']
        valor = entry.get(attribute, '')  # Cambia 'prec' al atributo deseado

        # Tratar casos especiales
        if valor.lower() == 'ip':
            valor = '0'
        else:
            valor = valor.replace(',', '.')

        # Crear una entrada para el indicativo si no existe
        if indicativo not in indicativos_data:
            indicativos_data[indicativo] = {}

        # Agregar el valor para la fecha y el indicativo
        indicativos_data[indicativo][fecha] = valor

    # Escribir los datos en el CSV
    with open(output, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)

        # Escribir la cabecera del CSV
        header = ['FECHA'] + list(indicativos_data.keys())
        writer.writerow(header)

        # Escribir los datos para cada fecha
        fechas = set()
        for indicativo, valores in indicativos_data.items():
            fechas.update(valores.keys())

        for fecha in sorted(fechas):
            row = [fecha]
            for indicativo in indicativos_data.keys():
                # Obtener el valor del indicativo para la fecha actual
                valor = indicativos_data[indicativo].get(fecha, '')
                row.append(valor)

            writer.writerow(row)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistics component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath", 
        type=str, 
        required=True, 
        help="Path to the input CSV File", 
        default="/mnt/shared/input.json"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--attribute",
        type=str,
        default="prec",
        required=True,
        help="Name of the date column.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/mnt/shared/output.csv",
        required=False,
        help=" Name of the output CSV file.",
    )

    args = parser.parse_args()
    
    # Call the main function with provided arguments and specify the output file path
    main(
        args.filepath,
        args.output,
        args.attribute,
        args.delimiter
    )
