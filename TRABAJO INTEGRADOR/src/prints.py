from constants import VIVIENDASPROPIAS, TOTALVIVIENDAS, OCUPSINBAÑO


def imprimirprocesar1(ultimos_trim):
    for año in sorted(ultimos_trim.keys()):
        trim, datos = ultimos_trim[año]
        saben = datos["saben"]
        no_saben = datos["no_saben"]
        total = saben + no_saben

        porcentaje_saben = (saben / total) * 100
        porcentaje_no_saben = (no_saben / total) * 100
        print(f"Año {año} (Trimestre {trim}):")
        print(f"  Porcentaje que sabe leer y escribir: {porcentaje_saben:.2f}%")
        print(f"  Porcentaje que NO sabe leer y escribir: {porcentaje_no_saben:.2f}%")


def imprimirprocesar4(ranking):
    for pos, elem in enumerate(ranking, start=1):
        aglomerado = elem[0]
        porcentaje = elem[1]
        print(f"{pos}. Aglomerado {aglomerado}: {porcentaje:.2f}%")


def imprimirprocesar5y6(dic_aglomerados):
    print("/" * 10, "Viviendas ocupadas por los propietarios", "/" * 10)
    for aglomerado, valores in dic_aglomerados.items():
        print(
            f"-Aglomerado {aglomerado}: {((valores[VIVIENDASPROPIAS] / valores[TOTALVIVIENDAS])* 100):.2f}%"
        )
    maximo = max(dic_aglomerados.items(), key=lambda x: x[1][2])
    print(
        f"El aglomerado con mayor cantidad de viviendas con más de dos ocupantes y sin baño es {maximo[0]} con un total de {maximo[1][OCUPSINBAÑO]} viviendas."
    )


def imprimirprocesar7(dic_aglomerados):
    for agl in dic_aglomerados:
        if dic_aglomerados[agl][0] > 0:
            print(
                f"aglomerado: {agl} tiene {dic_aglomerados[agl][1]} personas que hayan cursado al menos en nivel universitario o superior."
            )
        terciario = dic_aglomerados[agl][1] / dic_aglomerados[agl][0] * 100
        if terciario > 0:
            print(
                f"aglomerado: {agl} tiene {terciario:.2f}% que  hayan cursado al menos en nivel universitario o superior."
            )


def imprimirprocesar8(regiones_ordenadas):
    print("Región | % Personas en hogares inquilinos")
    for region, porcentaje in regiones_ordenadas:
        print(f"{region}     | {porcentaje:.2f}%")


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


def imprimirprocesar9(aglomerado):
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


def imprimirprocesar10(diccionario, a, b):
    total = 0
    cumple = 1
    print(f"{'Año':^10}{'Trimestre':^15}{'Aglomerado A':>23}{'Aglomerado B':>20}")
    print("-" * 71)
    for año, trimestres in diccionario.items():
        for trimestre, aglomerados in trimestres.items():
            porcentaje_a = (
                diccionario[año][trimestre][a][cumple]
                / diccionario[año][trimestre][a][total]
                * 100
            )
            porcentaje_b = (
                diccionario[año][trimestre][b][cumple]
                / diccionario[año][trimestre][b][total]
                * 100
            )
            print(
                f"{año:^10}{trimestre:^15}{porcentaje_a:>19.2f}%{porcentaje_b:>19.2f}%"
            )


def imprimirprocesar12(jubilados_por_aglomerado):
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
