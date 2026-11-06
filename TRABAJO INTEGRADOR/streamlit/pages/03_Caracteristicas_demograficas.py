from src.modulos_streamlit.P3.graficos_pag_3 import (
    grafico_mediana_y_media_edad,
    grafico_edad_promedio_x_aglomerado,
    grafico_distribucion_poblacion,
    graficar_dependencia_demografica,
)
from src.modulos_streamlit.P3.funciones_pag_3 import (
    calcular_dependencia_demografica,
    obtener_aglomerados,
)
from src.modulos_streamlit.P5.funciones_pag_5 import obtener_periodos_disponibles
from src.verificador import evaluar

import streamlit as st
import pandas as pd
from src.constants import INDIVIDUAL_FILE

st.title("Características Demográficas")
st.markdown(
    "*En esta sección se visualizará información relacionada a la características demográficas de la población argentina según la EPH.*"
)
st.divider()

if not evaluar(INDIVIDUAL_FILE):
    st.warning(
        "Los datos no están bien cargados, por favor asegúrese de que todo está en orden e intentelo nuevamente."
    )

else:

    tabs = st.tabs(
        [
            "Distribución de la población",
            "Edad promedio por aglomerado",
            "Dependencia Demográfica",
            "Edad media y mediana",
        ]
    )

    with tabs[0]:
        # Gráfico de la distribución de la población
        st.subheader("Distribución de la población")
        st.write(
            "El siguiente gráfico muestra la distribución de la población por grupos de edad y sexo."
        )
        anio_trimestres_dict = obtener_periodos_disponibles(INDIVIDUAL_FILE)

        if anio_trimestres_dict:
            anios = sorted(anio_trimestres_dict.keys())
            anio = st.selectbox("Seleccione un año.", anios)

            trimestre = st.selectbox(
                "Seleccione un trimestre.", anio_trimestres_dict[anio]
            )

            figura = grafico_distribucion_poblacion(INDIVIDUAL_FILE, anio, trimestre)
            st.pyplot(figura)

    with tabs[1]:
        # Cargar el gráfico de promedio de edad por aglomerado (inciso 1.3.2)
        st.markdown("### Edad promedio por aglomerado")
        st.markdown(
            f"El siguiente gráfico muestra los 32 aglomerados de Argentina, "
            f"junto con la edad promedio para un período determinado."
        )

        grafico_edad, año, trimestre = grafico_edad_promedio_x_aglomerado(
            INDIVIDUAL_FILE
        )
        st.markdown(f"Período: {trimestre}° trimestre de {año}")
        st.pyplot(grafico_edad)

    with tabs[2]:
        st.subheader("Dependencia Demográfica")
        st.write(
            "El siguiente gráfico muestra la dependencia demográfica y su evolución, para un aglomerado elegido."
        )

        # Obtengo diccionario de aglomerados
        aglomerado_cod_nombre = obtener_aglomerados()

        # Lista de nombres para mostrar en el selectbox
        lista_nombres = list(aglomerado_cod_nombre.values())

        nombre_aglomerado = st.selectbox("Seleccione un aglomerado", lista_nombres)

        # Obtengo el código correspondiente al aglomerado elegido por el usuario
        indice_seleccionado = lista_nombres.index(nombre_aglomerado)
        cod_aglomerado = list(aglomerado_cod_nombre.keys())[indice_seleccionado]

        # Proceso los datos
        resultado = calcular_dependencia_demografica(INDIVIDUAL_FILE, cod_aglomerado)

        # Grafico y muestro el resultado
        fig = graficar_dependencia_demografica(resultado)
        st.pyplot(fig)

    with tabs[3]:
        # Cargar el gráfico de edad media y mediana
        st.subheader("Edad media y mediana")
        st.write(
            "El siguiente gráfico muestra la edad media y la mediana de los individuos por periodo (año - trimestre)."
        )
        grafico = grafico_mediana_y_media_edad(INDIVIDUAL_FILE)
        st.pyplot(grafico, clear_figure=True)
