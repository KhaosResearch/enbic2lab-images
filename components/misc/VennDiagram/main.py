from numpy import sort
import pandas as pd
from matplotlib_venn import venn3, venn3_circles
import matplotlib.pyplot as plt
import argparse

def main(filepath:str,output1:str,output2:str,delimiter=",",legend:str="True"):
    # Convertir a booleano
    legend = True if legend.lower() == "true" else False    # Cargar datos desde el archivo CSV
    data = pd.read_csv(filepath,sep=delimiter)
    # Obtener conjuntos a partir de columnas del DataFrame
    a = set(data[data.columns[0]])
    b = set(data[data.columns[1]])
    c = set(data[data.columns[2]])
    
    datos_unicos = set(data.stack())
    lista_datos_unicos = sort(list(datos_unicos))
    naturals_cabo_gata_all_list = [""] * len(lista_datos_unicos)
    naturals_alcornocales_list = [""] * len(lista_datos_unicos)
    naturals_sierra_nieves_all_list = [""] * len(lista_datos_unicos)

    for i in range(len(lista_datos_unicos)):
        if lista_datos_unicos[i] in data["Alcornocales"].values:
            naturals_alcornocales_list[i] = "Alcornocales"
        if lista_datos_unicos[i] in data["Cabo de Gata"].values:
            naturals_cabo_gata_all_list[i] = "Cabo de Gata"
        if lista_datos_unicos[i] in data["Sierra de las Nieves"].values:
            naturals_sierra_nieves_all_list[i] = "Sierra de las Nieves"
        # Verificar si la cadena termina con una coma y eliminarla si es necesario
    # Crear un DataFrame desde las listas
    csv_data = {"Species": lista_datos_unicos, "Alcornocales": naturals_alcornocales_list, "Sierra de las Nieves":naturals_sierra_nieves_all_list, "Cabo de Gata":naturals_cabo_gata_all_list}
    df = pd.DataFrame(csv_data)

    # Guardar el DataFrame como un archivo CSV
    df.to_csv(output1, index=False, sep=";")

    # Calcular intersecciones y diferencias
    only_a = len(a - b - c)
    only_b = len(b - a - c)
    only_c = len(c - a - b)
    only_a_b = len(a & b - c)
    only_a_c = len(a & c - b)
    only_b_c = len(b & c - a)
    a_b_c = len(a & b & c)

    if (legend==True):
        legend_col=None
    else:
        legend_col=data.columns
    # Crear el diagrama de Venn
    venn3(subsets=(only_a, only_b, only_a_b, only_c, only_a_c, only_b_c, a_b_c), set_labels=legend_col)
    # Añadir círculos y leyenda
    venn3_circles(subsets=(only_a, only_b, only_a_b, only_c, only_a_c, only_b_c, a_b_c))
    
    if (legend==True):
        # Crear la leyenda con los nombres reales de los conjuntos
        set_labels = [str(name) for name in data.columns]
        legend_labels = [set_labels[0],set_labels[1],f'{set_labels[0]} ∩ {set_labels[1]}',set_labels[2], f'{set_labels[0]} ∩ {set_labels[2]}', f'{set_labels[1]} ∩ {set_labels[2]}', f'{set_labels[0]} ∩ {set_labels[1]} ∩ {set_labels[2]}']
        # Posicionar y ajustar el tamaño de la leyenda
        plt.legend(labels=legend_labels, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize='small')

    # Mostrar el diagrama
    plt.show()

    # Guardar el diagrama como un archivo PDF
    plt.savefig(output2, bbox_inches='tight')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP Plot component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        default="/mnt/shared/natural_park_species.csv",
        required=True,
        help="Path to the input CSV file",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )

    parser.add_argument(
        "--legend",
        type=str,
        default="True",
        required=True,
        help="Legend in  Venn diagram",
    )

    parser.add_argument(
        "--output1",
        type=str,
        required=True,
        help="Path to the output CSV file ",
    )
    parser.add_argument(
        "--output2",
        type=str,
        required=True,
        help="Path to the output CSV file ",
    )

    args = parser.parse_args()
    # Call the main function with provided arguments and specify the output file path
    main(args.filepath,args.output1,args.output2, args.delimiter, args.legend)
