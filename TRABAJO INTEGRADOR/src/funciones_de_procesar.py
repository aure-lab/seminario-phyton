import csv
from .constants import (
    CODUSU,
    NRO_HOGAR,
    AGLOMERADO_INDIVIDUO,
    AGLOMERADO_HOGAR,
    NUM_AÑO,
    TRIMESTRE,
    NIVEL_ED,
    PONDERA_INDIVIDUO,
    PONDERA_HOGAR,
    HOGAR_FILE,
    INDIVIDUAL_FILE,
    CAT_INAC,
    COND_HABITABILIDAD,
)

# procesar 4


def obtener_periodo_reciente(path):
    """
    Recorre el archivo y calcula el año y trimestre más reciente.

    Args:
        path: ruta al archivo csv que voy a procesar, puede tomar dos valores: INDIVIDUAL_FILE y HOGAR_FILE.

    Returns:
        Una tupla (año, trimestre) que referencia al período más reciente encontrado.
    """
    max_año = -1
    max_trim = -1
    with open(path, "r", newline="", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip().split(";")
        idx_año = encabezado.index("ANO4")
        idx_trim = encabezado.index("TRIMESTRE")

        for linea in archivo:
            columnas = linea.strip().split(";")
            año = int(columnas[idx_año])
            trim = int(columnas[idx_trim])

            if (año > max_año) or (año == max_año and trim > max_trim):
                max_año = año
                max_trim = trim
    return (max_año, max_trim)


def contar_personas_nivel6(path, periodo_indiv):
    """
    Recorre el archivo de individuos y devuelve los hogares que tienen al menos 2 personas con nivel educativo 6 (superior universitario completo).

    Args:
        path: ruta al archivo de individuos.
        periodo_indiv: tupla (año, trimestre) con el período más reciente.

    Returns:
        Un diccionario con clave (CODUSU, NRO_HOGAR) y valor num de aglomerado, que solo incluye hogares con 2 o más personas con nivel educativo 6.
    """
    hogares_nivel6 = {}
    hogares_validos = {}
    with open(path, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)

        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])

            # Filtro, solo me interesan los datos del período más reciente
            if (año, trim) != periodo_indiv:
                continue

            if int(fila[NIVEL_ED]) != 6:
                continue
                
            codusu = fila[CODUSU]
            num_hogar = int(fila[NRO_HOGAR])
            aglomerado = int(fila[AGLOMERADO_INDIVIDUO])

            clave = (codusu, num_hogar)
            hogares_nivel6[clave] = hogares_nivel6.get(clave, 0) + 1

            # Si tiene 2 o más, guardo datos del hogar en otra estructura
            if hogares_nivel6[clave] == 2:
                hogares_validos[clave] = aglomerado
    return hogares_validos


def contar_hogares_por_aglomerado(path, periodo_hogar, hogares_validos):
    """
    Recorre el archivo de hogares y contabiliza los hogares que tienen al menos 2 personas con nivel educativo 6 (superior universitario completo) y
    la cantidad total de hogares por aglomerado.

    Args:
        path: Ruta al archivo de hogares.
        periodo_hogar: Tupla (año, trimestre) con el período más reciente.
        hogares_validos: Diccionario cuyas claves son tuplas (CODUSU, NRO_HOGAR) de hogares válidos, y sus valores indican el aglomerado.

    Returns:
        total_hogares: Diccionario que contabiliza la cantidad de hogares en total de cada aglomerado.
        hogares_validos_por_aglo: Diccionario que contabiliza la cantidad de hogares válidos por aglomerado
    """
    total_hogares = {}
    hogares_validos_por_aglo = {}

    with open(path, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)

        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])
            if (año, trim) != periodo_hogar:
                continue

            codusu = fila[CODUSU]
            nro_hogar = int(fila[NRO_HOGAR])
            aglomerado = int(fila[AGLOMERADO_HOGAR])
            pondera = int(fila[PONDERA_HOGAR])
            clave = (codusu, nro_hogar)

            # Sumo al total general de hogares el valor de pondera
            total_hogares[aglomerado] = total_hogares.get(aglomerado, 0) + pondera

            # Si ese (codusu, nro_hogar) está en hogares_validos, lo agrego al nuevo diccionario y le sumo pondera
            if clave in hogares_validos:
                hogares_validos_por_aglo[aglomerado] = (
                    hogares_validos_por_aglo.get(aglomerado, 0) + pondera
                )

    return total_hogares, hogares_validos_por_aglo


def calcular_ranking(hogares_validos_por_aglo, total_hogares):
    """
    Calcula el porcentaje de hogares válidos sobre el total de hogares por aglomerado y muestra un ranking con los primeros 5 aglomerados con mayor porcentaje.

    Args:
        hogares_validos_por_aglo: Diccionario que almacena la cantidad de hogares válidos por aglomerado.
        total_hogares: Diccionario que almacena la cantidad de hogares en total de cada aglomerado.

    Returns:
        ranking (tuple): Tupla con los 5 aglomerados y sus porcentajes, ordenado de mayor a menor.
    """
    porcentajes = {}

    for aglo in hogares_validos_por_aglo:
        total = total_hogares.get(aglo, 0)
        if total > 0:
            porcentaje = (hogares_validos_por_aglo[aglo] / total) * 100
            porcentajes[aglo] = porcentaje

    # Tomo el diccionario de porcentajes como una lista de tuplas, y lo ordeno de mayor a menor. Me quedo con los primeros 5
    ranking = sorted(porcentajes.items(), key=lambda x: x[1], reverse=True)[:5]
    return ranking


# procesar 12


def obtener_jubilados(ult_trimestre):
    """
    Recorre el archivo individuos y crea un diccionario de jubilados para un trimestre específico.

    Un jubilado se identifica por tener CAT_INAC == 1.
    La clave del diccionario es (codusu, nro_hogar) y el valor es su ponderador.

    Args:
        ult_trimestre: Tupla (año, trimestre) que indica el período a filtrar.

    Returns:
        jubilados: Diccionario que almacena los jubilados del período indicado.
    """
    jubilados = {}
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)

        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])

            if (año, trim) != ult_trimestre:
                continue
            if int(fila[CAT_INAC]) == 1:  # jubilado
                codusu = fila[CODUSU]
                num_hogar = int(fila[NRO_HOGAR])
                pondera = int(fila[PONDERA_INDIVIDUO])
                # Si es jubilado, agrego el hogar y su pondera al diccionario
                clave = (codusu, num_hogar)
                jubilados[clave] = pondera
    return jubilados


def cant_jubilados_aglomerado(ult_trimestre, jubilados):
    """
    Calcula la cantidad de jubilados por aglomerado, tanto el total de jubilados
    como los que viven en vivienda insuficiente.

    Args:
        ult_trimestre: Tupla (año, trimestre) que indica el período a filtrar.
        jubilados: Diccionario que almacena datos de hogar y cantidades ponderadas de jubilados.

    Returns:
        estadisticas_aglomerado: Diccionario con cantidades ponderadas de jubilados (el total y las
            que cumplen con condición de habitabilidad = 'Insuficiente')
    """
    estadisticas_aglomerado = {}
    with open(HOGAR_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)

        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])
            if (año, trim) != ult_trimestre:
                continue

            codusu = fila[CODUSU]
            num_hogar = int(fila[NRO_HOGAR])
            aglomerado = int(fila[AGLOMERADO_HOGAR])
            cond_habitabilidad = fila[COND_HABITABILIDAD]

            clave = (codusu, num_hogar)
            if clave in jubilados:
                pondera_indiv = jubilados[clave]

                if aglomerado not in estadisticas_aglomerado:
                    estadisticas_aglomerado[aglomerado] = {
                        "total_pondera": 0,
                        "insuf_pondera": 0,
                    }

                estadisticas_aglomerado[aglomerado]["total_pondera"] += pondera_indiv

                if cond_habitabilidad == "Insuficiente":
                    estadisticas_aglomerado[aglomerado][
                        "insuf_pondera"
                    ] += pondera_indiv
    return estadisticas_aglomerado


def mostrar_porcentajes(jubilados_por_aglomerado):
    """
    Calcula e imprime por aglomerado el porcentaje de jubilados que viven en vivienda insuficiente.

    Args:
        jubilados_por_aglomerado: Diccionario con cantidades ponderadas de jubilados.
    """
    for aglomerado, datos in jubilados_por_aglomerado.items():
        total = datos["total_pondera"]
        insuf = datos["insuf_pondera"]
        porcentaje = ((insuf / total) * 100) if total > 0 else 0
        print(
            f"Aglomerado {aglomerado}: {porcentaje:.2f}% de jubilados con vivienda insuficiente"
        )


# procesar 9


def inicializar(aglomerado_x_trim, aglomerado, año, trim, nivel):
    """Inicializa el diccionario con respecto al aglomerado, año, trimestre y nivel.

    Args:
        aglomerado_x_trim (dicc): estructura a actualizar.
        aglomerado (str): aglomerado de la fila.
        año (str): año a actualizar.
        trim (str): trimestre a actualizar.
        nivel (str): nivel educativo a actualizar.
    """
    if aglomerado not in aglomerado_x_trim:
        aglomerado_x_trim[aglomerado] = {}

    if año not in aglomerado_x_trim[aglomerado]:
        aglomerado_x_trim[aglomerado][año] = {}

    if trim not in aglomerado_x_trim[aglomerado][año]:
        aglomerado_x_trim[aglomerado][año][trim] = {}

    if nivel not in aglomerado_x_trim[aglomerado][año][trim]:
        aglomerado_x_trim[aglomerado][año][trim][nivel] = 0


def centrar(algo):
    """Centra hacia la izquierda un dato pasado por parametro

    Args:
        algo (str/int/float/etc): Tipo de dato simple listo para centrar.

    Returns:
        str: Retorna el str con la cantidad de espacios a poner.
    """
    espacios = 20
    if not isinstance(algo, str):
        algo = str(algo)
        espacios -= len(algo)
    else:
        espacios -= len(algo)
    return algo + " " * espacios


def imprimir(aglomerado):
    """Imprime la tabla del diccionario pasado por parametro.

    Args:
        aglomerado (dic): aglomerado a imprimir.
    """
    header = [
        "Año",
        "Trimestre",
        "Primario incompleto",
        "Primario completo",
        "Secundario Incompleto",
        "Secundario completo",
        "Superior univ. incompleto",
        "Superior univ. completo",
        "Sin instruccion",
        "Ns/Nr",
    ]
    for title in header:
        print(centrar(title), end="|")
    print("\n" + "-" * 200)
    for año, trimestre in aglomerado.items():
        for trim, niveles in trimestre.items():
            print("\n" + centrar(año), end="|")
            print(centrar(trim), end="|")
            for nivel in range(9):
                nivel = str(nivel)
                if nivel in niveles.keys():
                    print(centrar(niveles[nivel]), end="|")
                else:
                    print(centrar(0), end="|")
