from .funciones_pag_4 import baño_en_el_hogar, tipos_de_vivienda
import pandas as pd
import matplotlib.pyplot as plt
from .funciones_pag_4 import obtener_aglomerados

def grafico_hogar_con_baño_en_la_vivienda(dataframe):
    """
    Genera un gráfico de barras horizontal que muestra la proporción de hogares con baño dentro de la vivienda,
    desagregado por aglomerado (con nombre en lugar de código).

    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame que contiene información sobre los hogares, incluyendo las columnas necesarias
        para calcular la proporción de hogares con baño ('IV9', 'PONDERA' y 'AGLOMERADO').

    Returns
    -------
    matplotlib.figure.Figure
        Objeto Figure de matplotlib con el gráfico de barras generado.
    """
    nombre_aglomerados = obtener_aglomerados()

    df = baño_en_el_hogar(dataframe)
    df = df.sort_values("AGLOMERADO")
    df["Nombre Aglomerado"] = df["AGLOMERADO"].map(nombre_aglomerados)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(
        df["Nombre Aglomerado"],
        df["Proporcion de Hogares con baño dentro de la vivienda"],
        color="skyblue",
        edgecolor="black",
    )
    ax.set_xlabel("Proporción de Hogares con Baño (%)", fontsize=12)
    ax.set_ylabel("Aglomerado", fontsize=12)
    ax.set_title("Proporción de Hogares con Baño dentro de la Vivienda por Aglomerado", fontsize=14, weight="bold")
    plt.tight_layout()
    return fig

def grafico_regimen_de_tenencia(df_tenencia):
    """
    Genera un gráfico de líneas que muestra la evolución trimestral de la cantidad
    de hogares según el régimen de tenencia.

    Args:
        df_tenencia (DataFrame): DataFrame con los datos agrupados por trimestre y régimen de tenencia.

    Returns:
        Figure: Objeto de Matplotlib con el gráfico final.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    pivot_df = df_tenencia.pivot(index="TRIMESTRE", columns="Régimen de tenencia", values="Cantidad de hogares")

    # Dibujo una línea por régimen de tenencia
    for columna in pivot_df.columns:
        ax.plot(pivot_df.index, pivot_df[columna], marker="o", label=columna)
    
    ax.set_title("Evolución trimestral del régimen de tenencia", fontsize=13, weight="bold")
    ax.set_xlabel("Trimestre", fontsize=11)
    ax.set_ylabel("Cantidad de hogares", fontsize=11)
    ax.set_xticks([1, 2, 3, 4])
    ax.grid(True, linestyle="--", alpha=0.5) 
    ax.legend(title="Régimen", fontsize=8, loc="upper left")

    plt.tight_layout()
    return fig


def grafico_tipo_de_viviendas(df):
    """
    Genera un gráfico de torta que muestra la proporción de tipos de vivienda,
    omitiendo los porcentajes menores a 3%.

    Args:
        df (pd.DataFrame): Con columnas "Tipo de vivienda" y "Porcentaje (%)".

    Returns:
        Figure: Objeto de Matplotlib con el gráfico final.
    """

    df = df[df["Porcentaje (%)"] > 3]

    
    colores = ["#377eb8", "#ff7f00", "#4daf4a", "#f781bf", "#a65628"]

    fig, ax = plt.subplots(figsize=(8, 6))

    wedges, texts, autotexts = ax.pie(
        df["Porcentaje (%)"],
        colors=colores,
        autopct="%1.1f%%",
        textprops={"fontsize": 8, "weight": "medium"},
        startangle=90,
    )

    ax.set_title("Distribución de tipos de viviendas")

    ax.legend(
        wedges,
        df["Tipo de vivienda"],
        title="Tipo de vivienda",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=9,
        title_fontsize=10
    )

    plt.tight_layout()
    return fig
