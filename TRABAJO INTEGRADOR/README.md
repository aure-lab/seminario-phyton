# Trabajo Integrador - Seminario de Python - GRUPO 03

## Participantes

- Ferrante Gallo, Delfina
- Ferreira Santos, Enzo
- Ferreyra, Santiago
- Galian, Cristian Emmanuel
- Juarez, Santiago Ian

## Descripción del Proyecto

Este proyecto consiste en el **análisis**, **limpieza** y **consulta** de una base de datos real proporcionada por el **INDEC** (Instituto Nacional de Estadística y Censos de la República Argentina). Los datos procesados corresponden a **dos conjuntos de archivos**:

- **Archivos de individuos**
- **Archivos de hogares**

## 📂 Requisitos de los Datos

- Los archivos de datos deben descargarse desde el sitio oficial del INDEC:

  > [https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)

- **No se debe modificar el nombre original de los archivos descargados**, ya que el sistema depende de los nombres para su correcto funcionamiento.

- **Introducir cada PAR de archivos**, se considera que la carpeta `./files` no tiene inconsistencias en los datos de `Individuos` y `Hogares`.

- **Compatibilidad**: El sistema **no es compatible** con los archivos correspondientes al **4to trimestre del año 2024**, debido a cambios en las columnas y estructura de los datos.

- Los archivos descargados deben ser ubicados en la carpeta:

  > `./files`

## Ejecución del Proyecto

1. Instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

> Para este programa se recomienda utilizar un entorno virtual.

### 💻Como crear un entorno virtual

1. Para crearlo debreremos introducir en la terminal de confianza (como bash) lo siguiente:
   - Windows: py -m venv venv
   - linux/Mac: phyton -m venv venv
2. Para activar el entorno en `1.` debereos introducir:
   - Windows: venv\Scripts\activate
   - Linux: source venv/bin/activate

## ⚠️ Aclaraciones importantes sobre la estructura del proyecto

- En el módulo de **merge** (donde se combinan los archivos), es **obligatorio** que las importaciones de `constants` se hagan usando **import relativo**:

  ```python
  from .constants import FILE_DIRECTORY, DEFAULT_OUT, INDIVIDUAL_FILE, HOGAR_FILE
  ```

* En caso de que la pagina no funcione correctamente con este comando:
  **streamlit run streamlit/Inicio.py**
* Debería hacerlo con este:
  **py -m streamlit run streamlit/Inicio.py**
  > ❗ Esto es necesario para que la aplicación funcione correctamente en Streamlit, debido a cómo maneja los módulos y rutas.

---

## Algunas aclaraciones - Sección A

### Criterios para la columna `CONDICION_DE_HABITABILIDAD` (inciso 10)

Para evaluar la habitabilidad de las viviendas se creó una nueva columna llamada CONDICION_DE_HABITABILIDAD, la cual clasifica las viviendas en cuatro categorías:

- **Insuficiente**
- **Regular**
- **Saludable**
- **Buena**

Se utilizaron cinco columnas clave, cuyos valores son 1, 2 (y en algunos casos 3):

- `IV6`: disponibilidad de agua
- `IV7`: origen del agua
- `IV8`: presencia de baño/letrina
- `IV9`: ubicación del baño/letrina
- `IV10`: tipo de baño

#### Reglas de clasificación

- **Buena**

  - `IV6 = 1`
  - `IV7 = 1`
  - `IV8 = 1`
  - `IV9 = 1`
  - `IV10 = 1`

- **Saludable**

  - `IV6 ∈ [1, 2]`
  - `IV7 ∈ [1, 2]`
  - `IV8 = 1`
  - `IV9 ∈ [1, 2]`
  - `IV10 ∈ [1, 2]`

- **Regular**

  - `IV6 ∈ [2, 3]`
  - `IV7 = 2`
  - `IV8 = 1`
  - `IV9 ∈ [2, 3]`
  - `IV10 = 3`

- **Insuficiente**

  - `IV6 = 3`
  - `IV7 = 3`
  - `IV8 = 2`

---

## Algunas aclaraciones - Parte 2

### Configuración inicial: Ruta de los datos

Para que la aplicación funcione correctamente, es necesario **indicar la ubicación (path)** donde se encuentran los archivos de la EPH. Esta configuración se realiza desde la sección **"Carga de datos"** en el menú lateral izquierdo.

> 🗂️ **Archivos requeridos:**  
> Asegurate de que en la carpeta seleccionada se encuentren los siguientes archivos en formato `.txt`, descargados desde la [Encuesta Permanente de Hogares (EPH)](https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-31-84).  
> Los nombres deben seguir el formato:
>
> - `usu_hogar_TXXX.txt`
> - `usu_individual_TXXX.txt`
>
> Donde `TXXX` representa el trimestre y año (por ejemplo: `T223` es el segundo trimestre de 2023).

### ¿Dónde configurar la ruta?

Al final del menú lateral izquierdo, encontrarás la sección **"Configuración"**, donde deberás ingresar la **ruta de la carpeta local** que contiene los archivos `.txt`.  
Por ejemplo:

```
C:\Users\Nombre\project\files
```

Una vez ingresada, presioná el botón **"Guardar ruta"**.

### ⚠️ Validación de ruta

Si se ingresa una ruta inválida o no se encuentran los archivos requeridos, la aplicación mostrará el siguiente mensaje:

> **Seleccione una ruta correcta.**

### ❗ Error en pagina de inicio

Es probable que al querer ejecutar la pagina de streamlit, esta misma marque que no ha encontrado la carpeta `src`, para solucionarlo en `Inicio.py` debes copiar el siguiente codigo:

```
 Import sys
 Import os
 os.path.append(os.path.abspath(os.path.join(os.path.dirname(**file**),'..')))
```

---

## 🛠️ Herramientas utilizadas

- **Python >= 3.9** (desarrollado con Python 3.12.9)
- **Jupyter Notebook** – para pruebas en la parte 1
- **Pandas** - para manipulación y análisis de datos
- **Folium** - para visualización de mapas
- **Matplotlib** - para gráficos estadísticos
- **Streamlit** - para desarrollo de la aplicación web interactiva

---
