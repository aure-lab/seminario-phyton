import streamlit as st
import pandas as pd
import json
from src.constants import CORDS
from pathlib import Path
from src.verificador import evaluar
from src.constants import INDIVIDUAL_FILE
from src.modulos_streamlit.P3.funciones_pag_3 import obtener_aglomerados
from src.modulos_streamlit.P5.funciones_pag_5 import (
    obtener_periodos_disponibles,
    calcular_desocupados_por_nivel,
    color_tasa_desempleo,
    color_tasa_empleo,
    calcular_tasa_de_empleo,
    calcular_tasa_de_desempleo,
    calcular_empleo_por_tipo,
)
from src.modulos_streamlit.P5.graficos_pag_5 import (
    grafico_tasa_de_desempleo,
    grafico_desocupados_por_nivel,
    grafico_tasa_de_empleo,
    mapa_tasas,
    graficar_tabla_ocupacion,
)
import folium
from streamlit_folium import st_folium

st.title("Actividad y empleo")
st.divider()


if not evaluar(INDIVIDUAL_FILE):
    st.warning(
        "Los datos no están bien cargados, por favor asegúrese de que todo está en orden e intentelo nuevamente."
    )
else:
    tabs = st.tabs(
        [
            "Personas desocupadas",
            "Tasa de desempleo",
            "Tasa de empleo",
            "Personas ocupadas",
            "Mapa tasa de empleo y desempleo",
        ]
    )

    df = pd.read_csv(INDIVIDUAL_FILE, sep=";", low_memory=False)

    with tabs[0]:
        st.subheader("Personas desocupadas")
        st.write(
            "El siguiente gráfico muestra la cantidad de personas desocupadas"
            " según sus estudios alcanzados, para un año y trimestre seleccionado."
        )
        periodos_disponibles = obtener_periodos_disponibles(INDIVIDUAL_FILE)
        st.markdown("Seleccioná un año y trimestre")

        # Selectores de año y trimestre
        años = sorted(periodos_disponibles.keys())
        año_seleccionado = st.selectbox("Año", años)
        trimestres = periodos_disponibles[año_seleccionado]
        trimestre_seleccionado = st.selectbox("Trimestre", trimestres)

        df_resultado = calcular_desocupados_por_nivel(
            año_seleccionado, trimestre_seleccionado
        )
        fig = grafico_desocupados_por_nivel(
            df_resultado, año_seleccionado, trimestre_seleccionado
        )
        st.pyplot(fig)

    with tabs[1]:
        st.subheader("Tasa de desempleo por aglomerado")
        st.write(
            "El siguiente gráfico muestra la evolución del desempleo (tasa de desempleo)"
            " a lo largo del tiempo, para un aglomerado seleccionado o para todo el país."
        )
        # Obtengo diccionario de aglomerados
        aglomerado_cod_nombre = obtener_aglomerados()
        aglomerado_cod_nombre[0] = "nivel pais"

        # Lista de nombres para mostrar en el selectbox
        lista_nombres = list(aglomerado_cod_nombre.values())

        nombre_aglomerado = st.selectbox("Seleccione un aglomerado", lista_nombres)

        # Obtengo el código correspondiente al aglomerado elegido por el usuario
        indice_seleccionado = lista_nombres.index(nombre_aglomerado)
        cod_aglomerado = list(aglomerado_cod_nombre.keys())[indice_seleccionado]

        grafico = grafico_tasa_de_desempleo(df, cod_aglomerado)
        st.pyplot(grafico)

    with tabs[2]:
        st.subheader("Tasa de empleo por aglomerado")
        st.write(
            "El siguiente gráfico muestra la evolución del empleo (tasa de empleo)"
            " a lo largo del tiempo, para un aglomerado seleccionado o para todo el país."
        )
        # Obtengo diccionario de aglomerados
        aglomerado_cod_nombre = obtener_aglomerados()
        aglomerado_cod_nombre[0] = "nivel pais"

        # Lista de nombres para mostrar en el selectbox
        lista_nombres = list(aglomerado_cod_nombre.values())

        nombre_aglomerado = st.selectbox("Seleccione un aglomerado:", lista_nombres)

        # Obtengo el código correspondiente al aglomerado elegido por el usuario
        indice_seleccionado = lista_nombres.index(nombre_aglomerado)
        cod_aglomerado = list(aglomerado_cod_nombre.keys())[indice_seleccionado]

        grafico = grafico_tasa_de_empleo(df, cod_aglomerado)
        st.pyplot(grafico)

    with tabs[3]:
        st.subheader("Personas ocupadas y su tipo de ocupación por aglomerado")
        st.write(
            "La siguiente tabla muestra el total de personas ocupadas, y el porcentaje de personas "
            "con empleo estatal, privado y otro, según aglomerado."
        )

        df_resultado = calcular_empleo_por_tipo(df)
        tabla = graficar_tabla_ocupacion(df_resultado)

        columnas = [
            "Aglomerado",
            "Total_ocupados",
            "Empleo_estatal",
            "Empleo_privado",
            "Otro_tipo",
        ]
        st.table(tabla[columnas])

    with tabs[4]:
        st.subheader("Mapa de tasa de empleo y desempleo")
        st.text(
            "Esta sección marca un punto en el mapa en base a un aglomerado seleccionado y su color va a depender si la tasa seleccionada bajó o disminuyó:\n"
            "- Al elegir la tasa de empleo se deben ver puntos verdes en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Rojo en caso contrario.\n"
            "- Al elegir la tasa de desempleo se deben ver puntos rojos en los aglomerados cuya tasa de empleo aumentó con el correr del tiempo. Verde en caso contrario.\n"
        )
        aglomerados = obtener_aglomerados()

        tipo_tasa = st.radio("Seleccione el tipo de tasa", ["Empleo", "Desempleo"])

        choice = st.selectbox("seleccione un aglomerado", aglomerados.values())

        # obtengo el codigo del aglomerado seleccionado
        index = {v: k for k, v in aglomerados.items()}[choice]

        if tipo_tasa == "Empleo":
            quien = calcular_tasa_de_empleo(df, index).sort_values(
                by="PERIODO", ascending=True
            )
            color = color_tasa_empleo(quien)

        else:
            quien = calcular_tasa_de_desempleo(df, index).sort_values(
                by="PERIODO", ascending=True
            )
            color = color_tasa_desempleo(quien)

        st.write(quien)
        st_folium(mapa_tasas(choice, index, color))
