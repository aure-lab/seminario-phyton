import streamlit as st
from src.constants import HOGAR_FILE, CANASTA_FILE
from src.verificador import evaluar
from src.modulos_streamlit.P5.funciones_pag_5 import obtener_periodos_disponibles
import pandas as pd
from src.modulos_streamlit.P7.funciones_pag_7 import (
    filtrar_canasta,
    calcular_porcentajes,
)

st.title("Ingresos")
st.divider()
st.markdown(
    "*En esta sección se visualizará información relacionada a los ingresos de la población argentina según la EPH.*"
)

if not evaluar(HOGAR_FILE):
    st.warning(
        "Los datos no están bien cargados, por favor asegúrese de que todo está en orden e intentelo nuevamente."
    )
else:
    periodos_disponibles = obtener_periodos_disponibles(HOGAR_FILE)
    años = sorted(periodos_disponibles.keys())
    año_seleccionado = st.selectbox("Año", años)
    trimestres = periodos_disponibles[año_seleccionado]
    trimestre_seleccionado = st.selectbox("Trimestre", trimestres)

    df_hogares = pd.read_csv(HOGAR_FILE, sep=";", low_memory=False)
    df_canasta = pd.read_csv(CANASTA_FILE, sep=",", low_memory=False)

    df_filtrado = df_hogares[
        (df_hogares["ANO4"] == int(año_seleccionado))
        & (df_hogares["TRIMESTRE"] == int(trimestre_seleccionado))
        & (df_hogares["IX_TOT"] == 4)
    ]

    # crear columnas con año y mes
    df_canasta["indice_tiempo"] = pd.to_datetime(df_canasta["indice_tiempo"])
    df_canasta["Año"] = df_canasta["indice_tiempo"].dt.year
    df_canasta["Mes"] = df_canasta["indice_tiempo"].dt.month

    df_canasta_filtrado = filtrar_canasta(
        df_canasta, año_seleccionado, trimestre_seleccionado
    )

    porcentaje_pobres, porcentaje_indigentes, total_hogares = calcular_porcentajes(
        df_canasta_filtrado, df_filtrado
    )

    # Mostrar los resultados
    st.subheader(
        f"Resultados para {año_seleccionado} - Trimestre {trimestre_seleccionado}"
    )
    st.write(f"Total de hogares: {total_hogares:.2f}")
    st.write(f"Porcentaje de hogares pobres: {porcentaje_pobres:.2f}%")
    st.write(f"Porcentaje de hogares indigentes: {porcentaje_indigentes:.2f}%")
