import streamlit as st
from src.constants import PAGES_DIRECTORY
from pathlib import Path

st.title("EncuestAR.")
st.divider()
st.write(
    "Esta página recopila y procesa información de la EPH (Encuesta Permanente de Hogares), realizada por el INDEC (Instituto Nacional de Estadistica y Censos) y las DPE "
    "(Direcciones Provinciales de Estadística). Estas mismas son encuestas realizadas a los habitantes de nuestro país con el fin de conocer sobre las características "
    "socioeconómicas de la población."
)
st.divider()
st.write("-Podrás encontrar: ")
st.page_link(
    PAGES_DIRECTORY / "02_Carga_de_datos.py", label="Carga de Datos.", icon="📲"
)
st.page_link(
    PAGES_DIRECTORY / "03_Caracteristicas_demograficas.py",
    label="Características Demográficas",
    icon="📊",
)
st.page_link(
    PAGES_DIRECTORY / "04_Caracteristicas_de_la_vivienda.py",
    label="Características de la vivienda.",
    icon="🕶",
)
st.page_link(
    PAGES_DIRECTORY / "05_Actividad_y_empleo.py", label="Actividad y Empleo.", icon="📝"
)
st.page_link(PAGES_DIRECTORY / "06_Educacion.py", label="Educación.", icon="📚")
st.page_link(PAGES_DIRECTORY / "07_Ingresos.py", label="Ingresos.", icon="💸")
