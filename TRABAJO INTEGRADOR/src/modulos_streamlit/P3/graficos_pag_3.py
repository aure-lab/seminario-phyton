from .funciones_pag_3 import (
    edad_promedio_x_aglomerado,
    ultimo_periodo,
    media_ponderada,
    mediana_ponderada,
    obtener_aglomerados,
)
import matplotlib.pyplot as plt
import pandas as pd


def grafico_edad_promedio_x_aglomerado(path):
    """
    Genera un gráfico de barras con la edad promedio por aglomerado.

    Args:
        path (str): Ruta al archivo CSV de individuos.

    Return:
        - figura: Figura del gráfico para mostrar en Streamlit.
        - año (int): Último año disponible del path.
        - trimestre (int): Último trimestre disponible del path.
    """
    año, trimestre = ultimo_periodo(path)
    df = edad_promedio_x_aglomerado(path, año, trimestre)

    # Mapeo de códigos a nombres de aglomerados
    str_aglomerados = obtener_aglomerados()
    df["Aglomerado"] = df["Aglomerado"].map(str_aglomerados)

    # Ordenar por edad promedio ascendente
    df = df.sort_values("Edad Promedio", ascending=True)

    # Figura y gráfico
    figura, ax = plt.subplots(figsize=(10, 12))

    ax.barh(df["Aglomerado"], df["Edad Promedio"], color="#23516B", edgecolor="#062133")

    ax.set_xlabel("Edad Promedio", fontsize=12)
    ax.set_ylabel("Aglomerado", fontsize=12)
    ax.set_title("Edad Promedio por Aglomerado", fontsize=14, weight="bold")
    ax.invert_yaxis()
    plt.tight_layout()

    return figura, año, trimestre


def grafico_mediana_y_media_edad(path):
    """
    Genera un gráfico de línea con la evolución de la edad media y la mediana de edad
    por año y trimestre a partir de un archivo CSV.

    El CSV debe contener al menos las columnas 'ANO4' (año), 'TRIMESTRE' (trimestre),
    'CH06' (edad) y 'PONDERA' (peso para cálculo ponderado). Se calcula la media y mediana
    ponderada por año y trimestre, y luego se grafica la serie temporal.

    Args:
        path (str): Ruta al archivo CSV con los datos.

    Returns:
        matplotlib.pyplot: Objeto pyplot configurado con el gráfico listo para mostrar o guardar.
    """
    df = pd.read_csv(path, sep=";")
    resultados = []
    for (año, trimestre), grupo in df.groupby(["ANO4", "TRIMESTRE"]):
        media = media_ponderada(grupo)
        mediana = mediana_ponderada(grupo)
        resultados.append(
            {
                "AÑO": año,
                "TRIMESTRE": trimestre,
                "EDAD MEDIA": media,
                "MEDIANA EDAD": mediana,
            }
        )
    resumen = pd.DataFrame(resultados)
    # Convertir el año y trimestre a un formato de periodo
    resumen["periodo"] = (
        resumen["AÑO"].astype(str) + " T" + resumen["TRIMESTRE"].astype(str)
    )

    # Configurar el gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(
        resumen["periodo"],
        resumen["EDAD MEDIA"],
        marker="o",
        label="Edad Media",
        color="blue",
    )
    plt.plot(
        resumen["periodo"],
        resumen["MEDIANA EDAD"],
        marker="x",
        label="Mediana Edad",
        color="orange",
    )

    # Personalizar el gráfico
    plt.title("Edad Media y Mediana por Periodo")
    plt.xlabel("Periodo (año - trimestre)")
    plt.ylabel("Edad")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()

    return plt


def grafico_distribucion_poblacion(path, año, trimestre):
    """
    Genera un gráfico de barras dobles que muestra la distribución
        de la población por grupos de edad y sexo.

    Args:
        path (str): Ruta al archivo CSV de individuos.
        año (int): Año para filtrar los datos.
        trimestre (int): Trimestre para filtrar los datos.

    Return:
        fig: Grafico para mostrar en Streamlit
    """
    df = pd.read_csv(path, sep=";")

    # Filtrar por año y trimestre
    filtro = (df["ANO4"] == año) & (df["TRIMESTRE"] == trimestre)
    df_filtrado = df[filtro]

    # Crear grupos de edad
    bins = list(range(0, 101, 10)) + [150]  # 0-9, 10-19, ..., 100+
    labels = [f"{i}-{i+9}" for i in range(0, 100, 10)] + ["100+"]
    df_filtrado["grupo_edad"] = pd.cut(
        df_filtrado["CH06"], bins=bins, labels=labels, right=False
    )

    # Agrupar por grupo de edad y sexo
    df_agrupado = (
        df_filtrado.groupby(["grupo_edad", "CH04_str"])["PONDERA"]
        .sum()
        .unstack(fill_value=0)
    )

    # Ordenar grupos
    df_agrupado = df_agrupado.loc[labels]

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))
    df_agrupado.plot(kind="bar", ax=ax)

    # Personalizar gráfico
    ax.set_title(f"Distribución por Edad y Sexo - {año} T{trimestre}")
    ax.set_xlabel("Grupo de Edad")
    ax.set_ylabel("Cantidad de Personas (en millones).")
    ax.legend(title="Sexo")
    plt.tight_layout()

    return fig


def graficar_dependencia_demografica(resultado):
    """
    Genera un gráfico de líneas con la dependencia demográfica y su evolución
    en el tiempo de un aglomerado elegido.

    Args:
        resultado (dict): Estructura {año: {trimestre: porcentaje}}.

    Returns:
        fig: Figura para mostrar en Streamlit.
    """

    periodos = []
    valores = []

    for año in sorted(resultado.keys()):
        for trimestre in sorted(resultado[año].keys()):
            periodo = f"{año} T{trimestre}"
            valor = resultado[año][trimestre]
            periodos.append(periodo)
            valores.append(valor)

    # Creo figura
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(periodos, valores, marker="o", color="blue")

    # Personalizar gráfico
    ax.set_title("Índice de Dependencia Demográfica")
    ax.set_xlabel("Período (año - trimestre)")
    ax.set_ylabel("Dependencia (%)")
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
