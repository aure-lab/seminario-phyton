import streamlit as st
import os
from src.modulos_streamlit.rango_fechas import (
    desde_hasta,
    consistencia_de_datos,
    carga_de_datos,
)
from src.modulos_streamlit.path_config import cargar_config, guardar_config

st.title("Carga de Datos. ")
st.divider()

# Cargar configuración al iniciar
config = cargar_config()
current_path = config["files_path"]
st.sidebar.title("Configuración")
st.sidebar.markdown("🗂 Ruta de la carpeta `files`")
new_path = st.sidebar.text_input("Ruta actual:", value=current_path)

if st.sidebar.button("Guardar ruta"):
    config["files_path"] = new_path
    guardar_config(config)
    st.sidebar.success(f"Ruta actualizada: {new_path}")
    st.rerun()
if os.path.exists(current_path):
    comprobar = consistencia_de_datos(current_path)
    if comprobar[0]:
        if len(comprobar[1]) == 0:
            st.warning("Carpeta vacia.")
        else:
            st.write("Consistencia de datos exitosa.")
            desde, hasta = desde_hasta(comprobar[1])
            st.write(f"El sistema contiene información desde {desde} hasta el {hasta}.")
            carga_de_datos(current_path)

    else:
        for hogares in comprobar[1]:
            st.write(
                f"Faltan datos del año 20{hogares[2:]}, trimestre {hogares[1]}. \n -Archivo: usu_hogar_{hogares}"
            )
        for individuos in comprobar[2]:
            st.write(
                f"Faltan datos del año 20{individuos[2:]}, trimestre {individuos[1]}. \n -Archivo: usu_individual_{individuos}"
            )

    if st.button("Recargar dato."):
        st.rerun()  # Fuerza la recarga para mostrar los datos actualizados
else:
    st.warning("Seleccione una ruta correcta.")
