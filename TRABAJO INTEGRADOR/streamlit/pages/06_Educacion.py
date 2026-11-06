import streamlit as st
import pandas as pd
from src.verificador import evaluar
from src.constants import INDIVIDUAL_FILE
from src.modulos_streamlit.P4.funciones_pag_4 import cuantos_años
import matplotlib.pyplot as plt
from src.modulos_streamlit.P6.funciones_pag_6 import (
    contar_por_nivel_educativo,
    definir_rango_etario,
    calcular_nivel_educativo_comun_por_rango_etario,
    generar_ranking_dataframe,
    calcular_alfabetismo,
)
from src.modulos_streamlit.P6.graficos_pag_6 import grafico_nivel_ed

st.title("Educación")
st.divider()
st.markdown(
    "*En ésta sección se visualizará información relacionada al nivel de educación alcanzado por la población argentina según la EPH.*"
)

if not evaluar(INDIVIDUAL_FILE):
    st.warning(
        "Los datos no están bien cargados, por favor asegúrese de que todo está en orden e intentelo nuevamente."
    )
else:
    df_individuos = pd.read_csv(INDIVIDUAL_FILE, delimiter=";")

    tabs = st.tabs(
        [
            "Máximo nivel educativo alcanzado",
            "Nivel educativo común",
            "Top 5 aglomerados con estudios univ/sup",
            "Capaces e incapaces de leer y escribir",
        ]
    )

    with tabs[0]:
        st.subheader("Cantidad de personas según nivel educativo alcanzado.")
        st.write(
            "En el siguiente gráfico se muestra la cantidad de personas"
            " según su máximo nivel educativo alcanzado en base a un año elegido."
        )

        choice = st.selectbox("Seleccione un año.", cuantos_años(df_individuos))

        if choice != "Todos":
            df_filtrado = df_individuos[df_individuos["ANO4"] == int(choice)]
            conteo = contar_por_nivel_educativo(df_filtrado)
        else:
            conteo = contar_por_nivel_educativo(df_individuos)
        st.pyplot(grafico_nivel_ed(conteo, choice))

    with tabs[1]:
        st.subheader("Nivel educacional alcanzado más común por rango etario.")
        st.write(
            "En el siguiente gráfico se muestra el nivel educativo más común en base"
            " a un rango etario (o varios) seleccionado/s."
        )

        df = pd.read_csv(INDIVIDUAL_FILE, delimiter=";")

        df["RANGO_ETARIO"] = df["CH06"].apply(definir_rango_etario)

        # filtro las filas con edades menores a 20 años
        df = df[df["RANGO_ETARIO"].notna()]

        rango = st.multiselect(
            "Seleccione un rango etario.",
            ["20-29", "30-39", "40-49", "50-59", "60+"],
            default=["20-29", "30-39"],
        )

        df_filtrado = df[df["RANGO_ETARIO"].isin(rango)]

        comun = calcular_nivel_educativo_comun_por_rango_etario(df_filtrado)

        st.table(comun)

    with tabs[2]:
        st.subheader("Ranking de 5 aglomerados.")
        st.write(
            "En el siguiente gráfico se presenta el ranking de los 5 aglomerados con mayor"
            " porcentaje de hogares que cuentan con dos o más personas con estudios universitarios"
            " o superiores completos. La información fue calculada a partir del par de archivos más"
            " recientes disponibles."
        )
        st.write(
            "Podés visualizar la tabla directamente en esta página o descargarla en formato CSV."
        )
        df_ranking, periodo = generar_ranking_dataframe()

        with st.expander("Ver datos en tabla"):
            st.dataframe(df_ranking, use_container_width=True)

        st.write(
            "Nota: Datos calculados para el último período: Año ",
            periodo[0],
            ", trimestre ",
            periodo[1],
        )

        st.download_button(
            label="📥 Descargar Ranking",
            data=df_ranking.to_csv(index=False).encode("utf-8"),
            file_name="ranking_aglomerados.csv",
            mime="text/csv",
        )

    with tabs[3]:
        st.subheader("Porcentaje de personas capaces e incapaces de leer y escribir.")
        st.write(
            "En la siguiente tabla se muestra, año tras año, el porcentaje de personas mayores a 6 años que pueden o no leer y escribir."
        )

        resultado = calcular_alfabetismo(df_individuos)
        st.table(resultado)
