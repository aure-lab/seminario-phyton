def procesar(ronda, jugadores):
    """
    Procesa las rondas sumando el KDA de cada jugador ademas de calcular sus puntos y quien fue el mvp

    Args:
        ronda (dict): Ronda jugada
        jugadores (dict): Tabla de estadisticas de los jugadores
    """
    # Variable auxiliar necesaria para saber quien fue el MVP de la ronda
    puntos_x_jugador = {}
    for names in ronda.keys():
        for stats in ronda[names].keys():
            jugadores[names][stats] += ronda[names][stats]
            pts = puntos(ronda[names])
        jugadores[names]["points"] += pts
        puntos_x_jugador[names] = pts
    jugadores[calcularMVP(puntos_x_jugador)]["MVPs"] += 1


def calcularMVP(puntos):
    """
    Calcula e imprime quien fue el MVP de la ronda en base a los puntos de cada jugador

    Args:
        puntos (dict): Nombre y puntos de cada jugador

    Returns:
        String: El nombre del jugador MVP
    """
    nombre = max(puntos.items(), key=lambda x: x[1])[0]
    print(" " * 20, f"el MVP de la partida fue {nombre}!")
    return nombre


def ordenar(jugadores):
    """ordena la tabla de stadisticas de los jugadores en base a sus puntos

    Args:
        jugadores (dict): Tabla de los jugadores

    Returns:
        tuple: La tabla ordenada
    """
    return sorted(jugadores.items(), key=lambda x: x[1]["points"], reverse=True)


def puntos(jugador):
    """
    Calcula los puntos que a obtenido un jugador

    Args:
        jugador (dict): Un jugador con sus estadisticas

    Returns:
        int: Cuantos puntos obtuvo dicho jugador
    """
    puntos_x_kill = 3
    puntos_x_asistencia = 1
    puntos_x_muerte = -1
    return (
        (jugador["kills"] * puntos_x_kill)
        + (jugador["assists"] * puntos_x_asistencia)
        + (jugador["deaths"] * puntos_x_muerte)
    )


def centrar(nombre):
    """
    Centra los nombres de los jugadores a mostrar en pantalla

    Args:
        nombre (string): Nombre del jugador

    Returns:
        int: La cantidad de espacios a agregar
    """
    return 15 - len(nombre)


def imprimir(jugadores):
    """Imprime la tabla de estadisticas en pantalla

    Args:
        jugadores (tuple): Tabla de los jugadores
    """
    espacios_de_tabla = 7
    espacios = 13
    print(
        "Jugador"
        + " " * espacios_de_tabla
        + "Kills"
        + " " * espacios_de_tabla
        + "Asistencias"
        + " " * espacios_de_tabla
        + "Muertes"
        + " " * espacios_de_tabla
        + "MVPs"
        + " " * espacios_de_tabla
        + "Puntos"
    )
    print("-" * 80)
    for nombre, stats in jugadores:
        print(
            f"{nombre}"
            + " " * centrar(nombre)
            + f'{stats["kills"]}'
            + " " * espacios
            + f' {stats["assists"]}'
            + " " * espacios
            + f'{stats["deaths"]}'
            + " " * espacios
            + f'{stats["MVPs"]}'
            + " " * espacios
            + f'{stats["points"]}'
        )
    print("-" * 80)
