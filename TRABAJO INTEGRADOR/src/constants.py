from pathlib import Path

# paths de distintas carpetas/archivos
DATA_PATH = Path(__file__).parent.parent
FILE_DIRECTORY = DATA_PATH / "files"
# path de salida(merge)
OUT_DIRECTORY = DATA_PATH / "data_out"
INDIVIDUAL_FILE = OUT_DIRECTORY / "individuales.csv"
HOGAR_FILE = OUT_DIRECTORY / "hogares.csv"
DEFAULT_OUT = OUT_DIRECTORY / "archCombinado.csv"
# path de archivos temporales
TEMP_FILE = DATA_PATH / "temp.csv"

# indices de columnas
AMBIENTES = 11
CAT_OCUP = 28
CH04 = 11
CH06 = 13
ESTADO = 27
HABITANTES = 64
IV6 = 16
IV7 = 17
IV8 = 19
IV9 = 20
IV10 = 21
NIVEL_ED = 26
V4 = 47

# indices seccion b
ANO4 = 1
II7 = 37
AGLOMERADO_HOGAR = 7
AGLOMERADO_INDIVIDUO = 8
PONDERA_HOGAR = 8
PONDERA_INDIVIDUO = 9
CH12 = 19
BAÑO = 41  # II9
HABITANTES = 64
NUM_AÑO = 1
TRIMESTRE = 2
EDAD_INDIV = 13
CH09 = 16
CH15 = 22
CH12 = 19
CODUSU = 0
NRO_HOGAR = 3
REGION = 5
CAT_INAC = 29
COND_HABITABILIDAD = 91
MATERIAL_TECHUMBRE = 89

# indices diccionario 5 y 6
TOTALVIVIENDAS = 0
VIVIENDASPROPIAS = 1
OCUPSINBAÑO = 2

# paths de streamlit
PAGES_DIRECTORY = DATA_PATH / "streamlit" / "pages"

# path del .json de coordenadas
CORDS = DATA_PATH / "aglomerados_coordenadas.json"

# path del .csv de valores de canasta
CANASTA_FILE = DATA_PATH / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"

# path de la configuracion de rutas
CONFIG_FILE = DATA_PATH / "config.json"