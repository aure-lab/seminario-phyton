import matplotlib.pyplot as plt
from .funciones_pag_5 import (
    calcular_tasa_de_desempleo,
    calcular_tasa_de_empleo,
)
from src.modulos_streamlit.P3.funciones_pag_3 import obtener_aglomerados
from src.constants import CORDS
import json
import folium


def grafico_desocupados_por_nivel(df_resultado, año, trimestre):
    """
    Genera un gráfico de barras que muestra la cantidad de personas desocupadas
    según su nivel educativo alcanzado.

    Args:
        df_resultado (pd.DataFrame): DataFrame con columnas 'NIVEL_ED' y 'Cantidad de personas',
        año (int): Año correspondiente a los datos visualizados.
        trimestre (int): Trimestre correspondiente a los datos visualizados.

    Returns:
        Fig (Mathplotlib.figure): Objeto que representa el gráfico generado.
    """

    # Mapeo de códigos a nombres de nivel educativo
    niveles_ed = {
        1: "Primario incompleto",
        2: "Primario completo",
        3: "Secundario incompleto",
        4: "Secundario completo",
        5: "Superior universitario incompleto",
        6: "Superior universitario completo",
        7: "Sin instrucción",
        9: "Ns/Nr",
    }

    df_resultado["Nivel educativo"] = df_resultado["NIVEL_ED"].map(niveles_ed)
    df_resultado = df_resultado[["Nivel educativo", "Cantidad de personas"]]

    colores = [
        "#93748A",  # Primario incompleto
        "#77BA99",  # Primario completo
        "#5C9096",  # Secundario incompleto
        "#F9D4BB",  # Secundario completo
        "#AA6F72",  # Superior univ. incompleto
        "#C8BFC7",  # Superior univ. completo
        "#80AF4E",  # Sin instrucción
        "#E0D68A",  # Ns/Nr
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Ordeno los datos por cantidad descendente
    df_resultado = df_resultado.sort_values("Cantidad de personas", ascending=True)

    barras = ax.barh(
        df_resultado["Nivel educativo"],
        df_resultado["Cantidad de personas"],
        color=colores[: len(df_resultado)],
    )

    for barra in barras:
        width = barra.get_width()
        ax.text(
            width + max(df_resultado["Cantidad de personas"]) * 0.01,
            barra.get_y() + barra.get_height() / 2,
            f"{int(width):,}",
            va="center",
            fontsize=9,
            weight="bold",
        )

    ax.set_title(
        f"Personas desocupadas según nivel educativo:\nAño {año} - Trimestre {trimestre}",
        fontsize=12,
        weight="bold",
    )

    ax.set_xlabel("Cantidad de personas")
    ax.set_ylabel("Nivel educativo")
    plt.tight_layout()
    return fig


def grafico_tasa_de_desempleo(df, aglomerado):
    """
    Genera un gráfico de la tasa de desempleo por periodo para un aglomerado específico.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos de empleo.
        aglomerado (int): Código del aglomerado para filtrar los datos.

    Returns:
        matplotlib.pyplot: Objeto pyplot configurado con el gráfico listo para mostrar o guardar.
    """
    df_tasa = calcular_tasa_de_desempleo(df, aglomerado)

    plt.figure(figsize=(12, 6))
    plt.plot(df_tasa["PERIODO"], df_tasa["TASA_DESEMPLEO"], marker="o", color="red")
    plt.title(f"Tasa de Desempleo en el Aglomerado {aglomerado}")
    plt.xlabel("Periodo")
    plt.ylabel("Tasa de Desempleo (%)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()

    return plt


def grafico_tasa_de_empleo(df, aglomerado):
    """
    Genera un gráfico de la tasa de desempleo por periodo para un aglomerado específico.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos de empleo.
        aglomerado (int): Código del aglomerado para filtrar los datos.

    Returns:
        matplotlib.pyplot: Objeto pyplot configurado con el gráfico listo para mostrar o guardar.
    """
    df_tasa = calcular_tasa_de_empleo(df, aglomerado)

    plt.figure(figsize=(12, 6))
    plt.plot(df_tasa["PERIODO"], df_tasa["TASA_EMPLEO"], marker="o", color="red")
    plt.title(f"Tasa de Empleo en el Aglomerado {aglomerado}")
    plt.xlabel("Periodo")
    plt.ylabel("Tasa de Empleo (%)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()

    return plt


def mapa_tasas(choice, index, color):
    """Genera el mapa a imprimir en base a un aglomerado.

    Args:
        choice (str): Nombre del aglomerado elegido.
        index (int): Codigo del aglomerado elegido.
        color (str): Color del punto del mapa.

    Returns:
        FoliumMap: Mapa a imprimir.
    """
    with open(CORDS, "r", encoding="utf-8") as file:
        dict_cords = json.load(file)

    cords = dict_cords[str(index).zfill(2)]["coordenadas"]

    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )

    tiles = "https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png"
    m = folium.Map(
        location=(-33.457606, -65.346857),
        control_scale=True,
        zoom_start=5,
        name="es",
        tiles=tiles,
        attr=attr,
    )

    folium.Marker(
        location=cords,
        popup=choice,
        tooltip="Clic para ver",
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(m)

    return m


def graficar_tabla_ocupacion(df_ocupacion):
    """
    Genera una tabla con el total de personas ocupadas y
    porcentajes de empleo estatal, privado y otro tipo por aglomerado.
    """

    aglomerados = obtener_aglomerados()

    # Mapear código a nombre
    df_ocupacion["Aglomerado"] = df_ocupacion["AGLOMERADO"].map(aglomerados)

    # Reordenar columnas para que el nombre quede primero
    df_final = df_ocupacion[
        [
            "Aglomerado",
            "Total_ocupados",
            "Empleo_estatal",
            "Empleo_privado",
            "Otro_tipo",
        ]
    ]

    return df_final
