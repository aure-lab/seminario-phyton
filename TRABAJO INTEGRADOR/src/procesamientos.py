import csv
from .constants import (
    CH12,
    AGLOMERADO_HOGAR,
    AGLOMERADO_INDIVIDUO,
    TOTALVIVIENDAS,
    VIVIENDASPROPIAS,
    OCUPSINBAÑO,
    PONDERA_HOGAR,
    PONDERA_INDIVIDUO,
    II7,
    HOGAR_FILE,
    BAÑO,
    HABITANTES,
    INDIVIDUAL_FILE,
    NUM_AÑO,
    TRIMESTRE,
    ESTADO,
    EDAD_INDIV,
    CH09,
    CH15,
    CH12,
    NIVEL_ED,
    CODUSU,
    NRO_HOGAR,
    REGION,
    CH06,
    NIVEL_ED,
    CAT_INAC,
    COND_HABITABILIDAD,
    ANO4,
    MATERIAL_TECHUMBRE,
)

from .funciones_de_procesar import (
    obtener_periodo_reciente,
    contar_personas_nivel6,
    contar_hogares_por_aglomerado,
    calcular_ranking,
    obtener_jubilados,
    cant_jubilados_aglomerado,
    inicializar,
)


def procesar1():
    """Esta funcion procesa el dataset de individuos y determina año a año el porcentaje de personas mayores a 6 años
    que saben y no saben leer y escribir, tomando solo el último trimestre disponible de cada año.
    """
    personas_por_periodo = {}
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)  # Omitir la cabecera
        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])
            edad = int(fila[EDAD_INDIV])
            alfabetizado = int(fila[CH09])
            pondera = float(fila[PONDERA_INDIVIDUO])

            if edad > 6:
                clave = (año, trim)
                if clave not in personas_por_periodo:
                    personas_por_periodo[clave] = {"saben": 0, "no_saben": 0}

                if alfabetizado == 1:
                    personas_por_periodo[clave]["saben"] += pondera
                elif alfabetizado == 2:
                    personas_por_periodo[clave]["no_saben"] += pondera

        # Reorganizo para quedarme solo con el último trimestre por año
        ultimos_trim = {}
        for (año, trim), datos in personas_por_periodo.items():
            if año not in ultimos_trim or trim > ultimos_trim[año][0]:
                ultimos_trim[año] = (trim, datos)

        return ultimos_trim


def procesar2(año_ingresado, trim_ingresado):
    """Esta funcion procesa el dataset de individuos, recibe un año y un trimestre ingresado
    por el usuario y calcula el porcentaje de personas no nacidas en Argentina
    que hayan cursado nivel universitario o superior en dicho año y trimestre.

    Args:
        año_ingresado: año elegido por el usuario.
        trim_ingresado: trimestre elegido por el usuario.
    """
    import csv

    if año_ingresado.isdigit() and trim_ingresado.isdigit():
        año_ingresado = int(año_ingresado)
        trim_ingresado = int(trim_ingresado)

        total = 0
        superior = 0
        with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
            reader = csv.reader(archivo, delimiter=";")
            next(reader)
            for fila in reader:
                año = int(fila[NUM_AÑO])
                trim = int(fila[TRIMESTRE])
                pais_nac = int(fila[CH15])
                nivel = int(fila[CH12])
                pondera = int(fila[PONDERA_INDIVIDUO])

                if año == año_ingresado and trim == trim_ingresado:
                    if pais_nac == 4 or pais_nac == 5:
                        total += pondera
                        if nivel == 7 or nivel == 8:
                            superior += pondera

            if total > 0:
                return (superior / total) * 100

    else:
        return None


def procesar3():
    """Procesa dataset de individuos y determina el período con menor desocupación de personas.

    Identifica las personas desocupadas, y construye un diccionario donde la clave es una tupla
    (año, trimestre) y el valor es la cantidad de personas desocupadas en ese período.
    """
    desocupados_por_periodo = {}
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)
        for fila in reader:
            año = int(fila[NUM_AÑO])
            trim = int(fila[TRIMESTRE])
            est = int(fila[ESTADO])

            if est == 2:
                # Tupla para acceder a cada año y trimestre
                clave = (año, trim)
                if clave not in desocupados_por_periodo:
                    desocupados_por_periodo[clave] = int(fila[PONDERA_INDIVIDUO])
                else:
                    desocupados_por_periodo[clave] += int(fila[PONDERA_INDIVIDUO])

        if desocupados_por_periodo:
            # Devuelve un iterable donde cada elemento es una tupla de tipo ((año, trimestre), cant_desocupados)
            menor_desoc = min(desocupados_por_periodo.items(), key=lambda x: x[1])
            return menor_desoc


def procesar4():
    """
    Procesa los archivos de hogares e individuos para generar un ranking de los 5 aglomerados
    con mayor porcentaje de hogares con dos o más personas con estudios universitarios completos.
    
    Returns:
        rank: Lista de tuplas con los 5 aglomerados con mayor porcentaje.
        periodo_hogar: Lista de tuplas que contiene el período más reciente (año, trimestre)
    """
    periodo_indiv = obtener_periodo_reciente(INDIVIDUAL_FILE)
    periodo_hogar = obtener_periodo_reciente(HOGAR_FILE)

    if periodo_indiv and periodo_hogar:
        print(
            f"Último período individuales: Año {periodo_indiv[0]}, trimestre {periodo_indiv[1]}"
        )
        print(
            f"Último período hogares: Año {periodo_hogar[0]}, trimestre {periodo_hogar[1]}"
        )
        hogares_validos = contar_personas_nivel6(INDIVIDUAL_FILE, periodo_indiv)

        total_hogares, hogares_validos_por_aglo = contar_hogares_por_aglomerado(
            HOGAR_FILE, periodo_hogar, hogares_validos
        )
        rank = calcular_ranking(hogares_validos_por_aglo, total_hogares)
        return rank, periodo_hogar
    else:
        print(
            "No se pudo obtener el período más reciente de alguno de los dos archivos."
        )


def procesar5(diccionario, fila):
    """Actualiza la informacion de un diccionario de aglomerados que guarda la cantidad de vivientas y tambien aquellas cuales solo sean ocupadas por sus propietarios
    (pos 0 y 1).

    Args:
        diccionario (dic): Informacion de los aglomerados.
        fila (list): Linea en mi archivo sobre la cual voy a actualizar mi diccionario.
    """
    # II7 -> 1 o 2 = propietario
    # regimen de tenencia
    valor = int(fila[PONDERA_HOGAR])
    # pos 0 = total pondera
    # pos 1 = total de propietarios por region
    diccionario[fila[AGLOMERADO_HOGAR]][TOTALVIVIENDAS] += valor
    if fila[II7] in ["1", "2"]:
        diccionario[fila[AGLOMERADO_HOGAR]][VIVIENDASPROPIAS] += valor


def armardic5y6():
    """Crea un diccionario separado por aglomerados y en base a este calcula:
    -De cada aglomerado el porcentaje de viviendas ocupadas por sus propietarios.
    -el aglomerado con mayor cantidad de viviendas con más de dos ocupantes y sin baño.
    """
    dic_aglomerados = {}
    with open(HOGAR_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)  # Saltar la primera fila (encabezados)
        for fila in reader:
            agl = fila[AGLOMERADO_HOGAR]
            if agl not in dic_aglomerados:
                dic_aglomerados[agl] = [0, 0, 0]
            procesar5(dic_aglomerados, fila)
            procesar6(dic_aglomerados, fila)
    return dic_aglomerados


def procesar6(diccionario, fila):
    """Actualiza la informacion de un diccionario de aglomerados que guarda datos de la cantidad de viviendas por aglomerado que tenganmás de dos ocupantes
    y sin baño. Informar también la cantidad de ellas.

    Args:
        diccionario (dic): Informacion de los aglomerados.
        fila (list): Linea en mi archivo sobre la cual voy a actualizar mi diccionario.
    """
    valor = int(fila[PONDERA_HOGAR])
    # II7 -> 4, 5, 6 o 7 = ocupante
    if (
        (fila[II7] in ["4", "5", "6", "7"])
        and (fila[BAÑO] == "4")
        and (int(fila[HABITANTES]) >= 2)
    ):
        diccionario[fila[AGLOMERADO_HOGAR]][OCUPSINBAÑO] += valor


def procesar7():
    """Crea un diccionario separado por aglomerados y en base a este calcula el porcentaje de personas que hayan cursado al
    menos en nivel universitario o superior.
    """
    dic_aglomerados = {}
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)
        for fila in reader:
            agl = fila[AGLOMERADO_INDIVIDUO]
            if agl not in dic_aglomerados:
                dic_aglomerados[agl] = [0, 0]
            dic_aglomerados[agl][0] += int(fila[PONDERA_INDIVIDUO])
            if fila[CH12] in ["7", "8"]:
                dic_aglomerados[agl][1] += int(fila[PONDERA_INDIVIDUO])
    return dic_aglomerados


def procesar8():
    """Calcula el porcentaje de inquilinos por región y las ordena de forma descendente.

    Returns: Lista de tuplas: (region, porcentaje)
    """
    personas_totales = {}
    personas_inquilinos = {}
    with open(HOGAR_FILE, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)

        for fila in reader:
            region = fila[REGION]
            tenencia = fila[II7]
            ix_tot = int(fila[HABITANTES])
            pondera = int(fila[PONDERA_HOGAR])

            personas = ix_tot * pondera

            #   Se acumula totales por región
            if region not in personas_totales:
                personas_totales[region] = 0
                personas_inquilinos[region] = 0

            personas_totales[region] += personas

            if tenencia == "3":
                personas_inquilinos[region] += personas

    # Se calcula y se ordena por porcentaje descendente
    regiones_ordenadas = []

    for region, total in personas_totales.items():
        inquilinos = personas_inquilinos[region]
        porcentaje = (inquilinos / total) * 100 if total > 0 else 0
        regiones_ordenadas.append((region, porcentaje))

    regiones_ordenadas.sort(key=lambda x: x[1], reverse=True)
    return regiones_ordenadas


def procesar9(seleccion):
    """Retorna una tabla que contiene la cantidad de personas mayores de edad segun sus estudios alcanzados (no acumulativa) del aglomerado seleccionado.

    Args:
        seleccion (str): Aglomerado sobre el cual se procesan los datos.
    """
    aglomerado_x_trim = {}
    with open(INDIVIDUAL_FILE) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            if int(row[CH06]) >= 18:
                aglomerado = row[AGLOMERADO_INDIVIDUO]
                año = row[ANO4]
                trim = row[TRIMESTRE]
                nivel = row[NIVEL_ED]
                pondera = int(row[PONDERA_INDIVIDUO])

                # Inicializar si no existen
                inicializar(aglomerado_x_trim, aglomerado, año, trim, nivel)

                aglomerado_x_trim[aglomerado][año][trim][nivel] += pondera
    if seleccion in aglomerado_x_trim.keys():
        return aglomerado_x_trim[seleccion]


def procesar10(a, b):
    """
    Lee un archivo CSV con datos individuales y calcula el porcentaje de personas
    mayores de 18 años con nivel educativo superior (nivel 3) para dos aglomerados
    seleccionados por el usuario, agrupado por año y trimestre.

    Muestra los resultados en una tabla por consola.

    Maneja errores si el archivo no existe, está vacío o no se puede leer.
    """
    with open(INDIVIDUAL_FILE, "r", newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo, delimiter=";")
        next(reader)
        aglomerados_deseados = [a, b]
        diccionario = {}
        solo_aglomerados = list(
            filter(
                lambda fila: fila[AGLOMERADO_INDIVIDUO] in aglomerados_deseados, reader
            )
        )
        total = 0
        cumple = 1
        if not solo_aglomerados:
            print("No hay datos para los aglomerados seleccionados.")
        elif (
            a in solo_aglomerados[AGLOMERADO_INDIVIDUO]
            and b not in solo_aglomerados[AGLOMERADO_INDIVIDUO]
        ):
            print(f"El aglomerado {b} no existe.")
        elif (
            b in solo_aglomerados[AGLOMERADO_INDIVIDUO]
            and a not in solo_aglomerados[AGLOMERADO_INDIVIDUO]
        ):
            print(f"El aglomerado {a} no existe.")
        else:
            for fila in solo_aglomerados:
                año = int(fila[NUM_AÑO])
                trim = int(fila[TRIMESTRE])
                aglo = fila[AGLOMERADO_INDIVIDUO]
                if año not in diccionario:
                    diccionario[año] = {}
                if trim not in diccionario[año]:
                    diccionario[año][trim] = {}
                if aglo not in diccionario[año][trim]:
                    diccionario[año][trim][aglo] = [0, 0]
                diccionario[año][trim][aglo][total] += int(fila[PONDERA_INDIVIDUO])
                if int(fila[CH06]) >= 18 and int(fila[NIVEL_ED]) == 3:
                    diccionario[año][trim][aglo][cumple] += int(fila[PONDERA_INDIVIDUO])
    return diccionario


def procesar11(seleccion):
    """Atraves de un año calcula el aglomerado con mayor y menor porcentaje de viviendas con material precario.

    Args:
        seleccion (str): Año seleccionado.
    """
    with open(HOGAR_FILE) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        # filtrar filas por el año seleccionado
        datos_x_año = [
            [
                row[ANO4],
                row[TRIMESTRE],
                row[AGLOMERADO_HOGAR],
                row[PONDERA_HOGAR],
                row[MATERIAL_TECHUMBRE],
            ]
            for row in reader
            if row[ANO4] == seleccion
        ]
    if datos_x_año == []:
        return None
    else:
        datos_x_año = sorted(datos_x_año, key=lambda x: x[1], reverse=True)
        ultimo = datos_x_año[0][1]
        datos_x_año = filter(lambda x: x[1] == ultimo, datos_x_año)
        aglomerados = {}
        for row in datos_x_año:
            pondera = int(row[3])
            aglomerado = row[2]
            techumbre = row[4]
            if aglomerado not in aglomerados:
                # [precarias, toltal]
                aglomerados[aglomerado] = [0, 0]
            aglomerados[aglomerado][1] += pondera
            if techumbre == "Material precario":
                aglomerados[aglomerado][0] += pondera
        min_aglomerado = min(
            aglomerados.items(), key=lambda x: (x[1][0] / x[1][1]) * 100
        )[0]
        max_aglomerado = max(
            aglomerados.items(), key=lambda x: (x[1][0] / x[1][1]) * 100
        )[0]
        return max_aglomerado, min_aglomerado


def procesar12():
    """
    Procesa ambos archivos y calcula e imprime el porcentaje de jubilados
    que viven en vivienda insuficiente por aglomerado en el último trimestre.
    """
    periodo_indiv = obtener_periodo_reciente(INDIVIDUAL_FILE)
    periodo_hogar = obtener_periodo_reciente(HOGAR_FILE)
    cant_jubilados = obtener_jubilados(periodo_indiv)
    jubilados_por_aglomerado = cant_jubilados_aglomerado(periodo_hogar, cant_jubilados)
    return jubilados_por_aglomerado


def procesar13(anio):
    """Procesa ambos archivos y cuenta las personas con nivel universitario o superior que viven en
    una vivienda con condiciones de habitabilidad insuficientes del último trimestre del año recibido
    por parámetro.

    Args:
        Anio(int): año ingresado por el usuario
    """

    if anio.isdigit():
        anio = int(anio)

        hogares_insuficientes = {}
        total = 0
        trimestres_disponibles = []

        # Leo archivo de hogares
        with open(HOGAR_FILE, "r", newline="", encoding="utf-8") as archivo_hogares:
            reader = csv.reader(archivo_hogares, delimiter=";")
            next(reader)
            for fila in reader:
                año = int(fila[ANO4])
                trim = int(fila[TRIMESTRE])
                condicion = fila[COND_HABITABILIDAD]

                if año == anio and condicion == "Insuficiente":
                    hogares_insuficientes[fila[CODUSU]] = True
                    if trim not in trimestres_disponibles:
                        trimestres_disponibles.append(trim)

        if trimestres_disponibles != []:
            # Saco el último trimestre disponible
            ultimo_trimestre = max(trimestres_disponibles)

            # Leo archivo de personas
            with open(
                INDIVIDUAL_FILE, "r", newline="", encoding="utf-8"
            ) as archivo_personas:
                reader = csv.reader(archivo_personas, delimiter=";")
                next(reader)
                for fila in reader:
                    año = fila[NUM_AÑO]
                    trim = int(fila[TRIMESTRE])
                    educ = int(fila[CH12])
                    codusu = fila[CODUSU]
                    pondera = int(fila[PONDERA_INDIVIDUO])

                    if año == anio and trim == ultimo_trimestre:
                        if educ in [6, 7, 8] and codusu in hogares_insuficientes:
                            total += pondera

            return ultimo_trimestre, total
    else:
        return None


if __name__ == "__main__":
    procesar9("-2")
