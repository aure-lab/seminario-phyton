from .constants import (
    HABITANTES,
    AMBIENTES,
    CH06,
    NIVEL_ED,
    V4,
    ESTADO,
    CAT_OCUP,
    CH04,
    IV6,
    IV7,
    IV8,
    IV9,
    IV10,
)

# -----------> traductores de "Individuales".


def traducir_ch04(fila):
    """Traduce a str la colmna CH04, originalmente de formato numerico (1: Masculino, 2:Femenino).

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna el sexo del individuo coincidente con la columna
    """
    return "Masculino" if int(fila[CH04]) == 1 else "Femenino"


def traducir_nivel_educacion(fila):
    """Traduce a str el formato numerico original de la columna NIVEL_ED siguiendo las siguientes reglas:
        - 1: "Primario incompleto".
        - 2: "Primario completo".
        - 3 "Secundario incompleto".
        - 4: "Secundario completo".
        - 5 a 6: "Superior o universitario".
        - 7 o 9: “Sin informacion”.

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna el nivel traducido.
    """
    valor = int(fila[NIVEL_ED])
    descripciones = {
        1: "Primario incompleto",
        2: "Primario completo",
        3: "Secundario incompleto",
        4: "Secundario completo",
        5: "Superior o Universitario",
        6: "Superior o Universitario",
        7: "Sin informacion",
        9: "Sin informacion",
    }
    resultado = descripciones[valor]
    return resultado


def traducir_condicion_laboral(fila):
    """Indica la condicion laboral del individuo basandose en las columnas ESTADO y CAT_OCUP segun las siguientes reglas:
        - Ocupado autónomo: si ESTADO es igual a 1 y CAT_OCUP es 1 o 2.
        - Ocupado dependiente: si ESTADO es igual a 1 y CAT_OCUP es 3 o 4 o 9.
        - Desocupado: si ESTADO es igual a 2.
        - Inactivo: si ESTADO es igual a 3.
        - Fuera de categoría/sin información: si ESTADO es igual a 4.

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna la condicion laboral coincidente con las condiciones previas
    """

    estado = int(fila[ESTADO])
    cat_ocup = int(fila[CAT_OCUP])

    match estado:
        case 1:
            if cat_ocup in [1, 2]:
                valor = "Ocupado autonomo"
            elif cat_ocup in [3, 4, 9]:
                valor = "Ocupado dependiente"
        case 2:
            valor = "Desocupado"
        case 3:
            valor = "Inactivo"
        # caso 4
        case _:
            valor = "Fuera de categoria/sin informacion"
    return valor


def traducir_universitario(fila):
    """Retorna en formato numerico si una persona mayor de edad ha completado el como mínimo el nivel universitario basandose en
        las columnas CH06 y NIVEL_ED (1:Sí, 0: No, 2: no aplica).

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        int: el valor numerico que le corresponde segun las reglas.
    """
    valor = 2
    if int(fila[CH06]) >= 18:
        if int(fila[NIVEL_ED]) == 6:
            valor = 1
        else:
            valor = 0
    return valor


# -----------> traductores de "Hogares".


def traducir_tipo_hogar(row):
    """Indica el tipo de hogar basandose en la columna HABITANTES bajo las siguientes reglas:
        -"Unipersonal" (una persona).
        -"Nuclear" (2 a 4 personas).
        -"Extendido" (5 o más personas).

    Args:
        row (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna el tipo que cumpla la condiciones previas.
    """
    if row[HABITANTES] == "1":
        tipo = "Unipersonal"
    elif row[HABITANTES] in ["2", "3", "4"]:
        tipo = "Nuclear"
    else:
        tipo = "Extendido"
    return tipo


def traducir_material_techumbre(fila):
    """Traduce a str el formato numerico original de la columna V4 bajo las siguientes condiciones:
        - 5 a 7: "Material precario".
        - 1 a 4: "Material durable".
        - 9: “No aplica”.

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna el str que cumpla con las condiciones previas.
    """
    valor = "no aplica"
    if int(fila[V4]) >= 5 and int(fila[V4]) <= 7:
        valor = "material precario"
    elif int(fila[V4]) >= 1 and int(fila[V4]) <= 4:
        valor = "material durable"
    return valor


def traducir_densidad_hogar(row):
    """Indica la densidad del hogar segun los habitantes por cada ambiente del hogar:
        - Bajo: menos de 1 persona por habitación.
        - Medio: entre 1 y 2 personas por habitación.
        - Alto: más de 2 personas por habitación.

    Args:
        row (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retornta la densidad que cumpla las condiciones previas.
    """
    cant = int(row[HABITANTES]) / int(row[AMBIENTES])
    if cant < 1:
        densidad = "Bajo"
    elif (cant >= 1) and (cant <= 2):
        densidad = "Medio"
    else:
        densidad = "Alto"
    return densidad


def traducir_condicion_habitabilidad(fila):
    """Indica cual es la condicion de habitibilidad segun las condiciones propuestas en el README.md.

    Args:
        fila (list): recibe la fila del archivo sobre la cual se trabaja.

    Returns:
        str: retorna la habitabilidad que coincida con las condiciones propuestas previamente.
    """
    agua = int(fila[IV6])
    origen_agua = int(fila[IV7])
    tiene_baño = int(fila[IV8])
    ubic_baño = int(fila[IV9])
    tipo_baño = int(fila[IV10])

    # Evaluacion de condiciones de habitabilidad: se definen variables booleanas para cada nivel

    condicion_saludable = (
        agua in [1, 2]
        and origen_agua in [1, 2]
        and tiene_baño == 1
        and ubic_baño in [1, 2]
        and tipo_baño in [1, 2]
    )

    condicion_regular = (
        agua in [2, 3]
        and origen_agua == 2
        and tiene_baño == 1
        and ubic_baño in [2, 3]
        and tipo_baño == 3
    )

    condicion_insuficiente = tiene_baño == 2 or (agua == 3 and origen_agua == 3)

    if condicion_insuficiente:
        resultado = "Insuficiente"
    elif condicion_regular:
        resultado = "Regular"
    elif condicion_saludable:
        resultado = "Saludable"
    else:
        resultado = "Buena"

    return resultado
