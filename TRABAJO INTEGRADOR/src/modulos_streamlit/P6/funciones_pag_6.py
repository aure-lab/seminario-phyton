import pandas as pd
from src.procesamientos import procesar4
from src.modulos_streamlit.P3.funciones_pag_3 import obtener_aglomerados


def contar_por_nivel_educativo(df_filtrado):
    """Crea una serie con los valores unicos del nivel y cuantas personas lo alcanzaron.

    Args:
        df_filtrado (Pandas.DataFrame): dataframe con la informacion del csv.

    Returns:                                                              _____________________________
        Pandas.Series: retorna una serie con la siguiente estructura----> |nivel: cantidad de personas|
                                                                          |___________________________|
    """

    conteo = df_filtrado["NIVEL_ED"].value_counts()

    nivel_dict = {
        1: "Primario incompleto",
        2: "Primario completo",
        3: "Secundario incompleto",
        4: "Secundario completo",
        5: "Superior universitario incompleto",
        6: "Superior universitario completo",
        7: "Sin instruccion",
        9: "Ns/Nr",
    }

    # Reemplazar claves por descripciones
    conteo.index = conteo.index.map(nivel_dict)

    return conteo


def definir_rango_etario(edad):
    """
    Asigna un rango etario basado en la edad.

    Parámetros:
    -----------
    edad : int o float
        Edad de la persona.

    Retorna:
    --------
    str o None
        Rango etario como string:
        - "20-29" para edades entre 20 y 29 años inclusive (29 excluido).
        - "30-39" para edades entre 30 y 39 años inclusive (39 excluido).
        - "40-49" para edades entre 40 y 49 años inclusive (49 excluido).
        - "50-59" para edades entre 50 y 59 años inclusive (59 excluido).
        - "60+" para edades mayores o iguales a 60 años.
        Devuelve None si la edad es menor a 20 o no cumple ninguna condición.
    """
    rango = None
    if 20 <= edad < 30:
        rango = "20-29"
    elif 30 <= edad < 40:
        rango = "30-39"
    elif 40 <= edad < 50:
        rango = "40-49"
    elif 50 <= edad < 60:
        rango = "50-59"
    elif edad >= 60:
        rango = "60+"
    return rango


def calcular_nivel_educativo_comun_por_rango_etario(df):
    """
    Calcula el nivel educativo más común por rango etario, ponderado por la variable 'PONDERA'.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que debe contener al menos las columnas:
        - 'RANGO_ETARIO': categoría de edad (string).
        - 'NIVEL_ED': código numérico del nivel educativo.
        - 'PONDERA': peso o ponderación de cada fila.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame con las columnas:
        - 'RANGO_ETARIO': rango etario.
        - 'NIVEL_ED': nivel educativo más común en texto (descriptivo).
        - 'PONDERA': suma de ponderaciones para ese nivel educativo y rango etario.
    """
    grupo = df.groupby(["RANGO_ETARIO", "NIVEL_ED"])["PONDERA"].sum().reset_index()

    maximo = grupo.groupby("RANGO_ETARIO")["PONDERA"].idxmax()

    comun = grupo.loc[maximo].reset_index(drop=True)

    obtener_nivel_educ = {
        1: "Primario incompleto",
        2: "Primario completo",
        3: "Secundario incompleto",
        4: "Secundario completo",
        5: "Superior universitario incompleto",
        6: "Superior universitario completo",
        7: "Sin instruccion",
        9: "Ns/Nr",
    }

    comun["NIVEL_ED"] = comun["NIVEL_ED"].map(obtener_nivel_educ)
    return comun


def generar_ranking_dataframe():
    """
    Ejecuta la función procesar4 (inciso 4 de la sección B del TI parte 1),
    convierte el resultado (ranking) en DataFrame y mapea nombres de aglomerado.

    Returns:
        pd.DataFrame: columnas ['Aglomerado', 'Porcentaje']
    """
    ranking, periodo = procesar4()
    if not ranking:
        return None

    # Convierto el ranking en un dataframe
    df = pd.DataFrame(ranking, columns=["Aglomerado", "Porcentaje"])

    # Mapeo de aglomerados con sus nombres
    nombres_aglo = obtener_aglomerados()
    df["Aglomerado"] = df["Aglomerado"].map(nombres_aglo)
    df["Porcentaje"] = df["Porcentaje"].round(2)

    return df, periodo


def calcular_alfabetismo(df):
    """
    Esta funcion calcula el porcentaje de personas mayores a 6 años capaces e incapaces de leer y escribir
        para cada año disponible.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que debe contener las columnas:
        - 'CH06' (edad)
        - 'CH09' (sabe leer o escribir: 1=sí, 2=no)
        - 'ANO4' (año)
        - 'PONDERA' (ponderador)

    Retorna:
    --------
    pandas.DataFrame
        DataFrame con columnas: ['AÑO', '% Capaces', '% Incapaces']
    """

    # Filtro el DataFrame
    df_filtrado = df[df["CH06"] > 6]

    resultados = []

    # Agrupo por año
    for año, datos_del_año in df_filtrado.groupby("ANO4"):

        total_ponderado = datos_del_año["PONDERA"].sum()
        capaces = datos_del_año[datos_del_año["CH09"] == 1]["PONDERA"].sum()
        incapaces = datos_del_año[datos_del_año["CH09"] == 2]["PONDERA"].sum()

        pct_capaces = (capaces / total_ponderado) * 100
        pct_incapaces = (incapaces / total_ponderado) * 100

        # Guardo el resultado de este año en la lista
        resultados.append(
            {"AÑO": año, "% Capaces": pct_capaces, "% Incapaces": pct_incapaces}
        )

    # Convierto la lista de resultados en un DataFrame ordenado por año
    resultados_df = pd.DataFrame(resultados).sort_values("AÑO").reset_index(drop=True)

    return resultados_df
