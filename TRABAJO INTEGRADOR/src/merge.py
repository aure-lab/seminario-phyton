import csv
import os
from .constants import (
    FILE_DIRECTORY,
    DEFAULT_OUT,
    INDIVIDUAL_FILE,
    HOGAR_FILE,
    OUT_DIRECTORY,
)


def diferenciarArch(path, start):
    """Agrega a una lista los archivos que empiecen con el parametro "start".

    Args:
        path (str): Path sobre el que busca los archivos.
        start (str): El nombre con el que tienen que empezar los archivos.

    Returns:
        list: Lista con todos los nombres de los archivos que cumplen dicha condicion
    """
    files = []
    for archivo in os.listdir(path):
        if archivo.startswith(start):
            files.append(archivo)
    return files


def UnirArchivos(archivos, PATH_FILE, salidaFinal=DEFAULT_OUT):
    """Une los archivos de la lista pasada por parametro y lo pone en el path de salidaFinal.

    Args:
        PATH_FILE(str): ruta sobre la cual busca los archivos.
        archivos (list): lista de los archivos a unir.
        salidaFinal (str): Path donde se guardan los archivos. Si no se coloca ninguna salida la salida default es DEFAULT_OUT
    """
    # si no existe la salida la crea
    os.makedirs(os.path.dirname(salidaFinal), exist_ok=True)

    ok = True
    with open(salidaFinal, "w", newline="", encoding="utf-8") as salida:
        writer = csv.writer(salida, delimiter=";")
        for archivo in archivos:
            ruta_archivo = os.path.join(PATH_FILE, archivo)
            if not os.path.exists(ruta_archivo):
                print(
                    f"no se pudo acceder al archivo {ruta_archivo}, si en la proxima ejecucion quieres incorporarlo trata asegurate de tener los permisos suficientes."
                )
                # saltea la otra parte del codigo
                continue
            if not os.access(ruta_archivo, os.R_OK):
                print(f"El archivo {ruta_archivo} no fue encontrado.")
                continue
            with open(ruta_archivo) as file:
                reader = csv.reader(file, delimiter=";")
                header = next(reader)
                if ok:
                    writer.writerow(header)
                    # ok controla que se escriba el encabezado una sola vez
                    ok = False
                for row in reader:
                    writer.writerow(row)


# si se quiere controlar el metodo por individual
if __name__ == "__main__":
    hogar = diferenciarArch(FILE_DIRECTORY, "usu_hogar")
    individual = diferenciarArch(FILE_DIRECTORY, "usu_individual")
    UnirArchivos(individual, INDIVIDUAL_FILE)
    UnirArchivos(hogar, HOGAR_FILE)
