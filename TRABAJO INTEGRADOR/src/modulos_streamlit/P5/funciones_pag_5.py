import pandas as pd
from src.constants import INDIVIDUAL_FILE


def obtener_periodos_disponibles(path):
    """
    Genera un diccionario con los años disponibles como claves y, para cada uno,
    una lista de trimestres disponibles según los datos cargados en el archivo.

    Args:
        path (str): Ruta al archivo CSV con todos los datos.

    Returns:
        dict: Diccionario con la estructura {año: [trimestres disponibles]}.
    """
    df = pd.read_csv(path, sep=";")

    disponibles = (
        df[["ANO4", "TRIMESTRE"]].drop_duplicates().sort_values(["ANO4", "TRIMESTRE"])
    )

    trimestres_por_año = {}
    for _, fila in disponibles.iterrows():
        anio = fila["ANO4"]
        trimestre = fila["TRIMESTRE"]
        trimestres_por_año.setdefault(anio, []).append(trimestre)

    return trimestres_por_año


def calcular_desocupados_por_nivel(año_selec, trimestre_selec):
    """
    Calcula la cantidad de personas desocupadas según su nivel educativo.

    Args:
        año_selec (int): Año seleccionado por el usuario.
        trimestre_selec (int): Trimestre seleccionado por el usuario.

    Returns:
        resultado (pd.Dataframe): Un DataFrame con dos columnas:
            - 'NIVEL_ED': Código del nivel educativo alcanzado.
            - 'Cantidad de personas': Suma ponderada de personas desocupadas para cada nivel educativo.
    """
    df = pd.read_csv(INDIVIDUAL_FILE, sep=";")

    # Filtro por año y trimestre seleccionados
    df_filtrado = df[(df["ANO4"] == año_selec) & (df["TRIMESTRE"] == trimestre_selec)]

    # Filtro personas desocupadas
    desocupados = df_filtrado[df_filtrado["ESTADO"] == 2]

    # Agrupo por nivel educativo y sumo pondera
    resultado = (
        desocupados.groupby("NIVEL_ED")["PONDERA"]
        .sum()
        .reset_index(name="Cantidad de personas")
        .sort_values("Cantidad de personas", ascending=False)
    )

    return resultado


def calcular_tasa_de_desempleo(df, aglomerado):
    """
    Calcula la tasa de desempleo (%) por período a partir de un DataFrame con datos individuales.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene la información individual. Debe tener al menos las columnas:
        - 'AGLOMERADO' : código del aglomerado geográfico
        - 'ESTADO'     : estado de actividad (1 = ocupado, 2 = desocupado)
        - 'PONDERA'    : factor de ponderación para cada registro
        - 'ANO4'       : año de la encuesta
        - 'TRIMESTRE'  : trimestre de la encuesta

    aglomerado : int
        Código del aglomerado para filtrar. Si es 0, calcula la tasa para todo el país.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame con columnas:
        - 'PERIODO'       : string concatenando año y trimestre (ejemplo: "2023 T1")
        - 'TASA_DESEMPLEO': tasa de desempleo en porcentaje para ese período

    Notas:
    ------
    La tasa de desempleo se calcula como:
        (Desocupados ponderados) / (Población económicamente activa ponderada) * 100
    donde la población económicamente activa (PEA) incluye ocupados y desocupados.
    """

    df_filtrado = df.copy()

    # filtro por aglomerado si no se seleccionó el nivel país
    if aglomerado != 0:
        df_filtrado = df[df["AGLOMERADO"] == aglomerado]

    # filtro por ocupados y desocupados
    df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin([1, 2])]

    # creo columna periodo
    df_filtrado["PERIODO"] = (
        df_filtrado["ANO4"].astype(str) + " T" + df_filtrado["TRIMESTRE"].astype(str)
    )

    agrupado = (
        df_filtrado.groupby("PERIODO")
        .apply(
            lambda x: pd.Series(
                {
                    "OCUPADOS": x[x["ESTADO"] == 1]["PONDERA"].sum(),
                    "DESOCUPADOS": x[x["ESTADO"] == 2]["PONDERA"].sum(),
                }
            )
        )
        .reset_index()
    )

    agrupado["TASA_DESEMPLEO"] = (
        agrupado["DESOCUPADOS"] / (agrupado["OCUPADOS"] + agrupado["DESOCUPADOS"])
    ) * 100

    return agrupado[["PERIODO", "TASA_DESEMPLEO"]]


def calcular_tasa_de_empleo(df, aglomerado):
    """
    Calcula la tasa de desempleo (%) por período a partir de un DataFrame con datos individuales.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene la información individual. Debe tener al menos las columnas:
        - 'AGLOMERADO' : código del aglomerado geográfico
        - 'ESTADO'     : estado de actividad (1 = ocupado, 2 = desocupado)
        - 'PONDERA'    : factor de ponderación para cada registro
        - 'ANO4'       : año de la encuesta
        - 'TRIMESTRE'  : trimestre de la encuesta

    aglomerado : int
        Código del aglomerado para filtrar. Si es 0, calcula la tasa para todo el país.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame con columnas:
        - 'PERIODO'       : string concatenando año y trimestre (ejemplo: "2023 T1")
        - 'TASA_DESEMPLEO': tasa de desempleo en porcentaje para ese período

    Notas:
    ------
    La tasa de desempleo se calcula como:
        (Desocupados ponderados) / (Población económicamente activa ponderada) * 100
    donde la población económicamente activa (PEA) incluye ocupados y desocupados.
    """

    df_filtrado = df.copy()

    # filtro por aglomerado si no se seleccionó el nivel país
    if aglomerado != 0:
        df_filtrado = df[df["AGLOMERADO"] == aglomerado]

    # filtro por ocupados y desocupados
    df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin([1, 2])]

    # creo columna periodo
    df_filtrado["PERIODO"] = (
        df_filtrado["ANO4"].astype(str) + " T" + df_filtrado["TRIMESTRE"].astype(str)
    )

    agrupado = (
        df_filtrado.groupby("PERIODO")
        .apply(
            lambda x: pd.Series(
                {
                    "DESOCUPADOS": x[x["ESTADO"] == 2]["PONDERA"].sum(),
                    "OCUPADOS": x[x["ESTADO"] == 1]["PONDERA"].sum(),
                }
            )
        )
        .reset_index()
    )

    agrupado["TASA_EMPLEO"] = (
        agrupado["OCUPADOS"] / (agrupado["OCUPADOS"] + agrupado["DESOCUPADOS"])
    ) * 100

    return agrupado[["PERIODO", "TASA_EMPLEO"]]


def color_tasa_desempleo(quien):
    """Define de que color se va a imprimir el punto en el mapa

    Args:
        quien (DataFrame): df con 2 columnas: "TASA_DESEMPLEO" y "PERIODO"

    Returns:
        str: color del punto.
    """
    if quien["TASA_DESEMPLEO"].iloc[0] < quien["TASA_DESEMPLEO"].iloc[-1]:
        return "red"
    else:
        return "green"


def color_tasa_empleo(quien):
    """Define de que color se va a imprimir el punto en el mapa

    Args:
        quien (DataFrame): df con 2 columnas: "TASA_EMPLEO" y "PERIODO"

    Returns:
        str: color del punto.
    """
    if quien["TASA_EMPLEO"].iloc[0] < quien["TASA_EMPLEO"].iloc[-1]:
        return "green"
    else:
        return "red"

def calcular_empleo_por_tipo(df):
    """
    Calcula para cada aglomerado el total de ocupados y el porcentaje
    de empleo estatal, privado y de otro tipo.

    Args:
        df (pd.DataFrame): DataFrame con datos individuales.

    Retorna:
        pd.DataFrame con columnas:
            - AGLOMERADO
            - Total_ocupados
            - Empleo_estatal
            - Empleo_privado
            - Otro_tipo
    """

    df_ocupados = df[df["ESTADO"] == 1]

    total_ocupados = df_ocupados.groupby("AGLOMERADO")["PONDERA"].sum()
    estatal = df_ocupados[df_ocupados["PP04A"] == 1].groupby("AGLOMERADO")["PONDERA"].sum()
    privado = df_ocupados[df_ocupados["PP04A"] == 2].groupby("AGLOMERADO")["PONDERA"].sum()
    otro = df_ocupados[df_ocupados["PP04A"] == 3].groupby("AGLOMERADO")["PONDERA"].sum()

    df_final = pd.DataFrame({
        "Total_ocupados": total_ocupados,
        "Empleo_estatal": estatal / total_ocupados * 100,
        "Empleo_privado": privado / total_ocupados * 100,
        "Otro_tipo": otro / total_ocupados * 100,
    }).reset_index()

    return df_final