import pandas as pd


def filtrar_canasta(df_canasta, año_seleccionado, trimestre_seleccionado):
    trimestre_meses = {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9], 4: [10, 11, 12]}
    meses = trimestre_meses[int(trimestre_seleccionado)]

    df_canasta_filtrado = df_canasta[
        (df_canasta["Año"] == int(año_seleccionado)) & (df_canasta["Mes"].isin(meses))
    ]

    return df_canasta_filtrado


def calcular_porcentajes(df_canasta_filtrado, df_filtrado):
    # promedio de la canasta basica para todos los meses del trimestre
    canasta_promedio = df_canasta_filtrado.drop(
        columns=["indice_tiempo", "Año", "Mes"]
    ).mean()

    # Calcular el ingreso total del hogar
    total_hogares = df_filtrado["PONDERA"].sum()
    pobres = df_filtrado.loc[
        df_filtrado["ITF"] < canasta_promedio["linea_pobreza"], "PONDERA"
    ].sum()
    indigentes = df_filtrado.loc[
        df_filtrado["ITF"] < canasta_promedio["linea_indigencia"], "PONDERA"
    ].sum()

    # Calcular los porcentajes
    porcentaje_pobres = (pobres / total_hogares) * 100 if total_hogares > 0 else 0
    porcentaje_indigentes = (
        (indigentes / total_hogares) * 100 if total_hogares > 0 else 0
    )

    return porcentaje_pobres, porcentaje_indigentes, total_hogares
