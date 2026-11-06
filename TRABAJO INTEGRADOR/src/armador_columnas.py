import csv
import os
from .traductores import (
    traducir_ch04,
    traducir_nivel_educacion,
    traducir_condicion_laboral,
    traducir_universitario,
    traducir_tipo_hogar,
    traducir_material_techumbre,
    traducir_densidad_hogar,
    traducir_condicion_habitabilidad,
)

from .constants import TEMP_FILE, INDIVIDUAL_FILE, HOGAR_FILE


def armar_columnas_ind():
    """Arma las columnas de Individuales pedidas en el tp integrador del archivo Individuales.csv"""
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as f_in, open(
        TEMP_FILE, "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.reader(f_in, delimiter=";")
        writer = csv.writer(f_out, delimiter=";")
        encabezado = next(reader)
        encabezado.extend(
            ["CH04_str", "NIVEL_ED_str", "CONDICION_LABORAL", "UNIVERSITARIO"]
        )  # agrega las nuevas columnas
        writer.writerow(encabezado)
        for fila in reader:
            fila.extend(
                [
                    traducir_ch04(fila),
                    traducir_nivel_educacion(fila),
                    traducir_condicion_laboral(fila),
                    traducir_universitario(fila),
                ]
            )  # se agregan los datos de las nuevas columnas
            writer.writerow(fila)
    try:
        os.replace(TEMP_FILE, INDIVIDUAL_FILE)
    except PermissionError:
        print(
            f"el archivo fue cargado con exito pero no tiene permisos para escribir sobre la ruta: {INDIVIDUAL_FILE}. \n Si desea ver el archivo, este se encuentra en: {TEMP_FILE}."
        )


def armar_columnas_hog():
    """Arma las columnas de Hogares pedidias en el tp integrador del archivo Hogares.csv"""
    with open(HOGAR_FILE, "r", newline="", encoding="utf-8") as f_in, open(
        TEMP_FILE, "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.reader(f_in, delimiter=";")
        writer = csv.writer(f_out, delimiter=";")
        encabezado = next(reader)
        encabezado.extend(
            [
                "TIPO_HOGAR",
                "MATERIAL_TECHUMBRE",
                "DENSIDAD_HOGAR",
                "CONDICION_DE_HABITABILIDAD",
            ]
        )  # agrega las nuevas columnas
        writer.writerow(encabezado)
        for fila in reader:
            fila.extend(
                [
                    traducir_tipo_hogar(fila),
                    traducir_material_techumbre(fila),
                    traducir_densidad_hogar(fila),
                    traducir_condicion_habitabilidad(fila),
                ]
            )  # se agregan los datos de las nuevas columnas
            writer.writerow(fila)
    try:
        os.replace(TEMP_FILE, HOGAR_FILE)
    except PermissionError:
        print(
            f"el archivo fue cargado con exito pero no tiene permisos para escribir sobre la ruta: {HOGAR_FILE}. \n Si desea ver el archivo, este se encuentra en: {TEMP_FILE}."
        )
