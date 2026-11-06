import streamlit as st
import pandas as pd
from src.constants import HOGAR_FILE
from src.verificador import evaluar
from src.modulos_streamlit.P4.funciones_pag_4 import (
    cuantos_años,
    hogares_entrevistados,
    material_predominante_pisos,
    obtener_regimen_tenencia,
    evolucion_regimen_de_tenencia,
    cond_de_habitabilidad,
    tipos_de_vivienda,
    viviendas_en_villa_de_emergencia,
)
from src.modulos_streamlit.P4.graficos_pag_4 import (
    grafico_hogar_con_baño_en_la_vivienda,
    grafico_regimen_de_tenencia,
    grafico_tipo_de_viviendas,
)
from src.modulos_streamlit.P3.funciones_pag_3 import obtener_aglomerados

st.title("Características de la vivienda")
st.markdown(
    "*En esta sección se visualizará información relacionada a las características de las viviendas de la población argentina según la EPH.*"
)
st.divider()


if not evaluar(HOGAR_FILE):
    st.warning(
        "Los datos no estan bien cargados, por favor asegúrese de que todo está en orden e intentelo nuevamente."
    )

else:
    df_hogares = pd.read_csv(HOGAR_FILE, delimiter=";", low_memory=False)

    choice = st.selectbox("Seleccione un año.", cuantos_años(df_hogares))
    if choice != "Todos":
        df_hogares = df_hogares[df_hogares["ANO4"] == int(choice)]

    tabs = st.tabs(
        [
            "Cantidad total de viviendas",
            "Tipos de viviendas",
            "Material de pisos",
            "Baño en el hogar",
            "Régimen de tenencia",
            "Villas de Emergencia",
            "Condición de Habitabilidad",
        ]
    )
    with tabs[0]:
        st.write(
            f"La cantidad de viviendas incluidas en esta encuesta son: {hogares_entrevistados(df_hogares)}"
        )

    with tabs[1]:
        st.subheader("Proporción de viviendas según su tipo")
        st.write(
            "El siguiente gráfico muestra la proporción de viviendas según su tipo."
            " Se omiten los tipos de vivienda con porcentaje menor al 3%."
        )
        df_tipos = tipos_de_vivienda(df_hogares)
        fig = grafico_tipo_de_viviendas(df_tipos)
        st.pyplot(fig)

    with tabs[2]:
        # Calculo material predominante de los pisos por aglomerado (inciso 1.4.3)
        df_materiales_aglomerado = material_predominante_pisos(df_hogares)

        st.subheader("Material predominante por aglomerado.")
        st.write(
            "La siguiente tabla muestra el material predominante en los pisos interiores"
            " de las viviendas, para cada aglomerado."
        )
        st.table(df_materiales_aglomerado.reset_index(drop=True))

    with tabs[3]:
        # calculo de baño en el hogar (inciso 1.4.4)
        st.subheader(
            "Proporción de hogares con baño dentro de la vivienda por aglomerado."
        )
        st.write(
            "El siguiente gráfico muestra la proporción de viviendas que disponen"
            " de baño dentro del hogar en el año seleccionado."
        )
        grafico = grafico_hogar_con_baño_en_la_vivienda(df_hogares)
        st.pyplot(grafico)

    with tabs[4]:
        # Calculo evolución de régimen de tenencia (inciso 1.4.5)
        st.subheader("Régimen de Tenencia")
        st.write(
            "El siguiente gráfico muestra la evolución del régimen de tenencia "
            "(propia, alquilada, cedida, etc.) para un aglomerado y año seleccionado."
        )

        # SELECTOR DE AGLOMERADOS
        # Obtengo diccionario de aglomerados
        aglomerado_cod_nombre = obtener_aglomerados()

        # Lista de nombres para mostrar en el selectbox
        lista_nombres = list(aglomerado_cod_nombre.values())
        nombre_aglomerado = st.selectbox("Seleccione un aglomerado", lista_nombres)

        # Obtengo el código correspondiente al aglomerado elegido por el usuario
        indice_seleccionado = lista_nombres.index(nombre_aglomerado)
        cod_aglomerado = list(aglomerado_cod_nombre.keys())[indice_seleccionado]

        # SELECTOR DE REGIMEN DE TENENCIA
        dic_tenencia = obtener_regimen_tenencia()

        tipos_tenencia = st.multiselect(
            "Seleccionar tipo(s) de tenencia",
            options=list(dic_tenencia.values()),
            placeholder="Seleccioná una, varias o todas las opciones",
        )

        df_tenencia = evolucion_regimen_de_tenencia(
            df_hogares, cod_aglomerado, tipos_tenencia
        )
        fig = grafico_regimen_de_tenencia(df_tenencia)
        st.pyplot(fig)

    with tabs[5]:
        # porcentaje de viviendas en villas de emergencia
        st.subheader("Porcentaje de viviendas en villas de emergencia")
        st.write(
            "La siguiente tabla muestra de manera decreciente la cantidad de viviendas ubicadas en villa"
            " de emergencia por aglomerado y el porcentaje con respecto al total, "
            "para un año seleccionado."
        )
        aglomerados = obtener_aglomerados()
        tabla = viviendas_en_villa_de_emergencia(df_hogares)
        tabla["AGLOMERADO"] = tabla["AGLOMERADO"].map(aglomerados)
        st.table(tabla)

    with tabs[6]:
        # porcentaje de viviendas por condicion de habitabilidad
        st.subheader('Porcentaje de viviendas por la condicion de "Habitabilidad"')
        st.text(
            "La siguiente tabla muestra el porcentaje de viviendas según su condición"
            " de Habitabilidad por cada aglomerado. Al finalizar, podrá encontrar un"
            " botón que permitirá descargar dicha tabla en formato CSV."
        )
        tabla = cond_de_habitabilidad(df_hogares)
        dic_aglomerados = obtener_aglomerados()
        tabla = tabla.reset_index()
        tabla["AGLOMERADO"] = tabla["AGLOMERADO"].replace(dic_aglomerados)
        st.table(tabla)

        st.download_button(
            label="Exportar a CSV.",
            data=tabla.to_csv(),
            file_name="porcentaje_x_cond.csv",
        )
