import os
import csv


def evaluar(path):
    """Evalua la existencia, acceso y la falta de contenido de un archivo.

    Args:
        path (str): Path del archivo a evaluar.

    Returns:
        boolean: Retorna si cumple con las condiciones previas o no.
    """
    ok = True
    # verifica si existe
    if os.path.exists(path):
        # verifica si tiene aSScceso al archivo
        if os.access(path, os.R_OK):
            with open(path) as file:
                reader1 = csv.reader(file, delimiter=";")
                # verifica si no esta vacio
                try:
                    next(reader1)
                except StopIteration:
                    print(
                        "El archivo esta vacio, asegurese de tener datos suficientes para completar la operacion."
                    )
                    return False
        else:
            ok = False
            print(
                "No se puede acceder al archivo, Porfavor compruebe sus permisos y vuelva a intentarlo."
            )
    else:
        ok = False
        print("Archivo inexistente.")
    return ok
