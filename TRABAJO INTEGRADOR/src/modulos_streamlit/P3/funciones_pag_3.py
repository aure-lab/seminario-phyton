import pandas as pd

def ultimo_periodo(path):
    """
    Lee el archivo de individuos y devuelve el último año y trimestre disponibles.
    
    Args:
        path (str): ruta al archivo CSV de individuos.
        
    Return:
        (int, int): una tupla con el último año y el último trimestre.
    """
    df = pd.read_csv(path, sep=";")
    ultimo_año = df["ANO4"].max()

    # Dentro del último año, busco el último trimestre
    ultimo_trim = df[df["ANO4"] == ultimo_año]["TRIMESTRE"].max()

    return ultimo_año, ultimo_trim

def edad_promedio_x_aglomerado(path, ultimo_año, ultimo_trim):
    """
    Calcula la edad promedio de las personas por aglomerado para el último año y trimestre disponibles.
    
    Args:
        path (str): ruta al archivo CSV de individuos.
        
    Return:
        DataFrame: con dos columnas: aglomerado y edad promedio.
    """
    df = pd.read_csv(path, sep=";")

    # Filtro
    df_filtro = df[(df["ANO4"] == ultimo_año) & (df["TRIMESTRE"] == ultimo_trim)]

    # Agrego columna donde calculo edad * pondera
    df_filtro['edad_x_pondera'] = df_filtro['CH06'] * df_filtro['PONDERA']
    grupos_x_aglomerado = df_filtro.groupby('AGLOMERADO')

    # Sumo edad ponderada y pondera general para cada aglomeraddo
    suma_edad_ponderada = grupos_x_aglomerado['edad_x_pondera'].sum()
    suma_pondera = grupos_x_aglomerado['PONDERA'].sum()

    # Calculo promedio
    edad_promedio = suma_edad_ponderada / suma_pondera

    # Paso a DataFrame y renombro columnas
    resumen = edad_promedio.reset_index()
    resumen.columns = ['Aglomerado', 'Edad Promedio']
    resumen['Edad Promedio'] = resumen['Edad Promedio'].round(2)

    return resumen

def año_trim_validos(path):
    """
    Obtiene los años y trimestres del archivo de individuos.
    
    Args:
        path (str): ruta al archivo CSV de individuos.
        
    Return:
        tupla: con dos listas, una de años válidos y otra de trimestres válidos.
    """
    df = pd.read_csv(path, sep=";")

    años_validos = df["ANO4"].unique().tolist()
    trimestres_validos = df["TRIMESTRE"].unique().tolist()

    return años_validos, trimestres_validos

def obtener_aglomerados():
    """
    Return:
        (dict): Devuelve un diccionario con los códigos y nombres de aglomerados.
    """
    return {
        2: "Gran La Plata",
        3: "Bahía Blanca-Cerri",
        4: "Gran Rosario",
        5: "Gran Santa Fe",
        6: "Gran Paraná",
        7: "Posadas",
        8: "Gran Resistencia",
        9: "Comodoro Rivadavia-Rada Tilly",
        10: "Gran Mendoza",
        12: "Corrientes",
        13: "Gran Córdoba",
        14: "Concordia",
        15: "Formosa",
        17: "Neuquén-Plottier",
        18: "Santiago del Estero-La Banda",
        19: "Jujuy-Palpalá",
        20: "Río Gallegos",
        22: "Gran Catamarca",
        23: "Gran Salta",
        25: "La Rioja",
        26: "Gran San Luis",
        27: "Gran San Juan",
        29: "Gran Tucumán-Tafí Viejo",
        30: "Santa Rosa-Toay",
        31: "Ushuaia-Río Grande",
        32: "Ciudad Autónoma de Buenos Aires",
        33: "Partidos del Gran Buenos Aires",
        34: "Mar del Plata",
        36: "Río Cuarto",
        38: "San Nicolás-Villa Constitución",
        91: "Rawson-Trelew",
        93: "Viedma-Carmen de Patagones"
    }

def calcular_dependencia_demografica(path, cod_aglomerado):
    """
    Esta función calcula el índice de dependencia demográfica por cada año y trimestre.

    Args:
        path (str): Ruta al archivo CSV de individuos.
        cod_aglomerado (int): Código del aglomerado elegido por el usuario.

    Returns:
        (dict): Diccionario con estructura {año: {trimestre: porcentaje}}.
    """

    df = pd.read_csv(path, sep=";")
    df = df[df["AGLOMERADO"] == cod_aglomerado]

    resultado = {}

    for (año, trimestre), grupo in df.groupby(["ANO4", "TRIMESTRE"]):
        mayores = grupo[grupo["CH06"] >= 65]["PONDERA"].sum()
        menores = grupo[grupo["CH06"] <= 14]["PONDERA"].sum()
        activos = grupo[(grupo["CH06"] >= 15) & (grupo["CH06"] <= 64)]["PONDERA"].sum()

        dependencia = (menores + mayores) / activos * 100

        if año not in resultado:
            resultado[año] = {}
        resultado[año][trimestre] = dependencia

    return resultado

def mediana_ponderada(grupo):
    """
    Calcula la mediana ponderada de la columna 'CH06' para un grupo dado.

    La mediana ponderada es el valor donde la suma acumulada de los pesos ('PONDERA') 
    alcanza al menos la mitad del total de pesos del grupo.

    Args:
        grupo (pd.DataFrame): DataFrame con al menos las columnas 'CH06' (edad) y 'PONDERA' (peso).

    Returns:
        float: Valor de la mediana ponderada de 'CH06'.
    """
    ordenado = grupo.sort_values("CH06").reset_index(drop=True)
    ordenado["pesos_acumulados"] = ordenado["PONDERA"].cumsum()
    mitad = ordenado["PONDERA"].sum() / 2
    mediana = ordenado[ordenado["pesos_acumulados"] >= mitad].iloc[0]["CH06"]
    return mediana
    
def media_ponderada(grupo):
    """
    Calcula la media ponderada de la columna 'CH06' para un grupo dado.

    La media ponderada se calcula como la suma de los productos de cada valor por su peso,
    dividido por la suma total de los pesos.

    Args:
        grupo (pd.DataFrame): DataFrame con al menos las columnas 'CH06' (edad) y 'PONDERA' (peso).

    Returns:
        float: Valor de la media ponderada de 'CH06'. Retorna 0 si la suma de pesos es cero.
    """
    total = grupo["PONDERA"].sum()
    suma = sum(grupo["CH06"] * grupo["PONDERA"])
    return suma / total if total > 0 else 0