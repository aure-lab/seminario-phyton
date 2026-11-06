import matplotlib.pyplot as plt


def grafico_nivel_ed(conteo, año):
    """crea un grafico de barras dependiendo el nivel educativo y la cantidad de personas que lo alcanzaron.

    Args:
        conteo (Pandas.Series): Estructura organizada en base a las caracteristicas mencionadas anteriormente.
        año (int): Año seleccionadado.

    Returns:
        matplotlib.figure.Figure: Grafico.
    """
    fig, ax = plt.subplots(figsize=(10, 6))  # Crear figura y eje

    conteo.plot(
        kind="barh",  # ← barra horizontal
        ax=ax,
        title=f"Nivel educativo alcanzado en {año}",
        xlabel="Cantidad de personas",
        ylabel="Nivel educativo",
    )

    plt.tight_layout()

    return fig
