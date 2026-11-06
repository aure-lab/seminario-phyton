import pandas as pd
from src.modulos_streamlit.P3.funciones_pag_3 import obtener_aglomerados


def cuantos_años(df_hogares):
    """
    Genera una lista de los años disponibles en el dataset.

    Args:
        df_hogares (DataFrame): Dataset completo o filtrado.

    Returns:
        list: Lista ordenada de años disponibles en el dataset más la opción "Todos".
    """
    return sorted(df_hogares["ANO4"].unique().tolist()) + ["Todos"]


def hogares_entrevistados(df_hogares):
    """
    Calcula la cantidad total ponderada de viviendas incluidas en el dataset.

    Args:
        df_hogares (DataFrame): Dataset ya filtrado por año o sin filtrar.

    Returns:
        float: Suma de la variable de ponderación que representa hogares entrevistados.
    """
    return df_hogares["PONDERA"].sum()


def material_predominante_pisos(df_hogares):
    """
    Calcula, para cada aglomerado, el material predominante en los pisos interiores
    de las viviendas utilizando la ponderación.

    Args:
        df_hogares (DataFrame): Dataset ya filtrado por año o sin filtrar.

    Returns:
        DataFrame: DataFrame con columnas 'AGLOMERADO' y 'Material Predominante',
                   mostrando el material predominante en pisos interiores por aglomerado.
    """

    agrupado = df_hogares.groupby(["AGLOMERADO", "IV3"])["PONDERA"].sum().reset_index()

    # Para cada aglomerado, busco el índice donde 'pondera' es mayor
    max_material_x_aglomerado = agrupado.groupby("AGLOMERADO")["PONDERA"].idxmax()

    # Me quedo solo con el material predominante de cada aglomerado y lo ordeno
    resultado = agrupado.loc[
        max_material_x_aglomerado, ["AGLOMERADO", "IV3"]
    ].sort_values("AGLOMERADO")

    materiales = {
        1: "Mosaico / Baldosa / Madera / Cerámica / Alfombra",
        2: "Cemento / Ladrillo fijo",
        3: "Ladrillo suelto / Tierra",
    }

    aglomerados = obtener_aglomerados()

    # Reemplazo valores numéricos por strings
    resultado["Material Predominante"] = resultado["IV3"].map(materiales)
    resultado["AGLOMERADO"] = resultado["AGLOMERADO"].map(aglomerados)
    # Elimino la columna IV3
    resultado = resultado[["AGLOMERADO", "Material Predominante"]]

    return resultado


def baño_en_el_hogar(df_hogares):
    """
    Calcula el porcentaje de hogares con baño dentro de la vivienda, ponderado por aglomerado.

    Parameters
    ----------
    df_hogares : pandas.DataFrame
        DataFrame que contiene información sobre los hogares, incluyendo las columnas
        'IV9' (indicador de baño en la vivienda), 'PONDERA' (ponderador) y 'AGLOMERADO'.

    Returns
    -------
    pandas.DataFrame
        DataFrame con dos columnas: 'AGLOMERADO' y 'Proporcion de Hogares con baño dentro de la vivienda',
        que indica el porcentaje ponderado de hogares con baño dentro por cada aglomerado.
    """
    df = df_hogares.copy()
    df["tiene_baño"] = df["IV9"] == 1
    agrupado = df.groupby("AGLOMERADO")
    proporciones = (
        agrupado.apply(
            lambda x: (x["tiene_baño"] * x["PONDERA"]).sum() / x["PONDERA"].sum()
        )
        * 100
    )
    aglomerados = obtener_aglomerados()
    resultado = proporciones.reset_index()
    resultado.columns = [
        "AGLOMERADO",
        "Proporcion de Hogares con baño dentro de la vivienda",
    ]

    return resultado


def obtener_regimen_tenencia():
    """
    Return:
        (dict): Devuelve un diccionario con valores y significados de cada regimen de tenencia.
    """
    return {
        1: "Propietario de la vivienda y el terreno",
        2: "Propietario de la vivienda solamente",
        3: "Inquilino / arrendatario de la vivienda",
        4: "Ocupante por pago de impuestos / expensas",
        5: "Ocupante en relación de dependencia",
        6: "Ocupante gratuito (con permiso)",
        7: "Ocupante de hecho (sin permiso)",
        8: "Está en sucesión",
    }


def evolucion_regimen_de_tenencia(df_hogares, cod_aglomerado, tenencias_seleccionadas):
    """
    Calcula la evolución trimestral del régimen de tenencia de viviendas
    para un aglomerado y año específico.

    Args:
        df_hogares (DataFrame): Dataset de hogares ya filtrado por año o sin filtrar.
        cod_aglomerado (int): Código del aglomerado seleccionado.
        tenencias_seleccionadas (list): Lista de regímenes seleccionados. Si está vacía, se incluyen todos.

    Returns:
        DataFrame: DataFrame con columnas 'TRIMESTRE', 'Régimen de tenencia' y 'Cantidad de hogares'.
    """

    dic_tenencia = obtener_regimen_tenencia()

    # Filtro por aglomerado
    df = df_hogares[df_hogares["AGLOMERADO"] == cod_aglomerado].copy()

    # Reemplazo los códigos por su str
    df["Régimen de tenencia"] = df["II7"].map(dic_tenencia)

    # Filtro por regímenes seleccionados (si no están todos)
    if tenencias_seleccionadas:
        df = df[df["Régimen de tenencia"].isin(tenencias_seleccionadas)]

    # Agrupo por trimestre y régimen, sumo pondera
    resultado = (
        df.groupby(["TRIMESTRE", "Régimen de tenencia"])["PONDERA"]
        .sum()
        .reset_index()
        .rename(columns={"PONDERA": "Cantidad de hogares"})
        .sort_values("TRIMESTRE")
    )

    return resultado


def cond_de_habitabilidad(df_hogares):
    """
    Calcula el porcentaje ponderado de hogares según su condición de habitabilidad, por aglomerado.

    Parameters
    ----------
    df_hogares : pandas.DataFrame
        DataFrame que contiene información sobre los hogares, incluyendo las columnas
        'AGLOMERADO', 'CONDICION_DE_HABITABILIDAD' y 'PONDERA'.

    Returns
    -------
    pandas.DataFrame
        DataFrame en formato pivot con los aglomerados como filas, las distintas condiciones
        de habitabilidad como columnas, y los valores representando el porcentaje ponderado
        de hogares en cada condición.
    """
    # cuento la cantidad del pondera por cada condicion en cada aglomerado
    cuantos_x_algo = (
        df_hogares.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"])["PONDERA"]
        .sum()
        .reset_index(name="pondera")
    )

    # cantidad de viviendas por aglomerado (sin tener en cuenta la cond)
    total = df_hogares.groupby("AGLOMERADO")["PONDERA"].sum().reset_index(name="total")

    df_ponderado = pd.merge(cuantos_x_algo, total, on="AGLOMERADO")
    df_ponderado["porcentaje_ponderado"] = (
        100 * df_ponderado["pondera"] / df_ponderado["total"]
    )

    return df_ponderado.pivot(
        index="AGLOMERADO",  # Las filas serán los aglomerados
        columns="CONDICION_DE_HABITABILIDAD",  # Las columnas serán las diferentes condiciones
        values="porcentaje_ponderado",  # Los valores son los porcentajes calculados
    ).fillna(
        0
    )  # rellena con 0 los que no tienen nada


def tipos_de_vivienda(df_hogares):
    """
    Calcula el porcentaje ponderado de cada tipo de vivienda según la columna 'IV1'.

    Args:
        df_hogares (pd.DataFrame): DataFrame con datos de hogares sin filtrar.

    Returns:
        pd.DataFrame: DataFrame con columnas 'Tipo de vivienda' y 'Porcentaje (%)'.
    """

    tipos_vivienda = {
        1: "Casa",
        2: "Departamento",
        3: "Pieza en inquilinato",
        4: "Pieza en hotel/pensión",
        5: "Local no construido para habitación",
    }

    # Calculo total para porcentaje
    total = df_hogares["PONDERA"].sum()

    # Agrupar por tipo de vivienda y sumar ponderaciones
    df_tipo = df_hogares.groupby("IV1")["PONDERA"].sum().reset_index()

    # Calculo porcentaje
    df_tipo["Porcentaje (%)"] = (df_tipo["PONDERA"] / total) * 100

    # Reemplazar los códigos por los nombres correspondientes
    df_tipo["Tipo de vivienda"] = df_tipo["IV1"].map(tipos_vivienda)

    # Ordeno de manera descendente
    df_tipo = df_tipo.sort_values(by="Porcentaje (%)", ascending=False)

    return df_tipo


def viviendas_en_villa_de_emergencia(df_hogares):
    """
    Calcula la cantidad de viviendas en villas de emergencia por aglomerado,
    así como el porcentaje de estas respecto al total de viviendas en cada aglomerado.

    Args:
        df_hogares (pd.DataFrame): DataFrame con datos de hogares.

    Returns:
        pd.DataFrame: DataFrame con columnas 'AGLOMERADO', 'Viviendas en villa de emergencia' y 'Porcentaje (%)'.
    """
    # Total de viviendas por trimestre, por aglomerado
    total_viviendas_por_aglomerado = (
        df_hogares.groupby(["AGLOMERADO"])["PONDERA"]
        .sum()
        .reset_index()
        .rename(columns={"PONDERA": "Total viviendas"})
    )

    # Viviendas en villa de emergencia (IV12_3 == 1) por aglomerado
    villas_df = df_hogares[df_hogares["IV12_3"] == 1]
    viviendas_villas = (
        villas_df.groupby(["AGLOMERADO"])["PONDERA"]
        .sum()
        .reset_index()
        .rename(columns={"PONDERA": "Viviendas en villa de emergencia"})
    )

    # Crear DataFrame con los resultados
    resultado = pd.merge(viviendas_villas, total_viviendas_por_aglomerado, on="AGLOMERADO")

    resultado["Porcentaje (%)"] = ((
        resultado["Viviendas en villa de emergencia"] / resultado["Total viviendas"]
    ) * 100)

    resultado = resultado.sort_values(
        by="Viviendas en villa de emergencia", ascending=False
    ).reset_index(drop=True)
    return resultado[
        ["AGLOMERADO", "Viviendas en villa de emergencia", "Porcentaje (%)"]
    ]
