import csv
from src.constants import FILE_DIRECTORY, HOGAR_FILE, INDIVIDUAL_FILE
from src.merge import diferenciarArch, UnirArchivos
from src.verificador import evaluar
from src.armador_columnas import armar_columnas_ind, armar_columnas_hog


def consistencia_de_datos(PATH):
    """Comprueba que haya un par de datos de individuos y hogar por cada trimestre descargado

    Args:
        PATH(str): path donde va a comprobar la consistencia de datos.

    Returns:
        tuple: POSICIONES----> 0: devuelve T o F si los archivos son consistentes.
                                |->EN CASO DE SER T:
                                |    1: Devuelve los trimestres y años de los archivos.
                                |->EN CASO DE SER F:
                                    1: Devuelve las inconsistencias de los archivos de Hogares.
                                    2: Devuelve las inconsistencias de los archivos de Individuos.
    """
    # se queda con el T... de los nombres de los archivos
    individual = set(
        map(
            lambda x: x.replace(".txt", "").split("_")[-1],
            diferenciarArch(PATH, "usu_individual"),
        )
    )
    hogares = set(
        map(
            lambda x: x.replace(".txt", "").split("_")[-1],
            diferenciarArch(PATH, "usu_hogar"),
        )
    )
    # si los 2 conjuntos son iguales entonces se confirma la consistencia de datos
    if hogares == individual:
        # El true en el ppal indica si se cumple o no la consistencia
        return (True, individual)
    # sino me fijo cuales estan en individuos que no estan en hogares y viceversa
    else:
        ind = hogares - individual
        hog = individual - hogares
        return (False, hog, ind)


def desde_hasta(trimestres):
    """Estaclece un rango entre fechas.

    Args:
        trimestres (set): trimestres disponibles(con sus años.)

    Returns:
        tuple: retorna la fechas del limite inferior y superior.
    """
    if trimestres:
        principios_de_trimestre = {"1": "1", "2": "4", "3": "7", "4": "10"}
        desde = min(trimestres, key=lambda x: x[2:] + x[1])
        hasta = max(trimestres, key=lambda x: x[2:] + x[1])
        desde = principios_de_trimestre[desde[1]] + "/20" + desde[2:]
        hasta = str((int(hasta[1]) * 3)) + "/20" + hasta[2:]
        return desde, hasta
    return None, None


def carga_de_datos(PATH_FILE):
    """Realiza la carga de datos a partir de los datasets de la carpeta files."""
    hogar = diferenciarArch(PATH_FILE, "usu_hogar")
    UnirArchivos(hogar, PATH_FILE, HOGAR_FILE)
    if evaluar(HOGAR_FILE):
        armar_columnas_hog()
    individual = diferenciarArch(PATH_FILE, "usu_individual")
    UnirArchivos(individual, PATH_FILE, INDIVIDUAL_FILE)
    if evaluar(INDIVIDUAL_FILE):
        armar_columnas_ind()
