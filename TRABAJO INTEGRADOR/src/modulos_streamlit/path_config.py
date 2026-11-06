from src.constants import CONFIG_FILE, FILE_DIRECTORY
import json
import os


def cargar_config():
    """Carga la configuracion de la carpeta donde se guardan los .txt del EPH/ si no existe devuelve la configuracion default.

    Returns:
       dict: diccionario con la ruta.
    """
    if not os.path.exists(CONFIG_FILE):
        return {"files_path": FILE_DIRECTORY}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def guardar_config(config):
    """Guarda la configuracion de la carpeta donde se guardan los txt de la EPH en un json.

    Args:
        config (dict): diccionario con el nuevo path.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
