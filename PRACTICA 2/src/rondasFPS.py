from procesarKDA import imprimir, procesar, ordenar

rounds = [
    {
        "Shadow": {"kills": 2, "assists": 1, "deaths": True},
        "Blaze": {"kills": 1, "assists": 0, "deaths": False},
        "Viper": {"kills": 1, "assists": 2, "deaths": True},
        "Frost": {"kills": 0, "assists": 1, "deaths": False},
        "Reaper": {"kills": 1, "assists": 1, "deaths": False},
    },
    {
        "Shadow": {"kills": 0, "assists": 2, "deaths": False},
        "Blaze": {"kills": 2, "assists": 0, "deaths": True},
        "Viper": {"kills": 1, "assists": 1, "deaths": False},
        "Frost": {"kills": 2, "assists": 1, "deaths": True},
        "Reaper": {"kills": 0, "assists": 1, "deaths": False},
    },
    {
        "Shadow": {"kills": 1, "assists": 0, "deaths": False},
        "Blaze": {"kills": 2, "assists": 2, "deaths": True},
        "Viper": {"kills": 1, "assists": 1, "deaths": True},
        "Frost": {"kills": 0, "assists": 1, "deaths": False},
        "Reaper": {"kills": 1, "assists": 1, "deaths": False},
    },
    {
        "Shadow": {"kills": 2, "assists": 1, "deaths": False},
        "Blaze": {"kills": 1, "assists": 0, "deaths": True},
        "Viper": {"kills": 0, "assists": 2, "deaths": False},
        "Frost": {"kills": 1, "assists": 1, "deaths": True},
        "Reaper": {"kills": 1, "assists": 1, "deaths": False},
    },
    {
        "Shadow": {"kills": 1, "assists": 2, "deaths": True},
        "Blaze": {"kills": 0, "assists": 1, "deaths": False},
        "Viper": {"kills": 2, "assists": 0, "deaths": True},
        "Frost": {"kills": 1, "assists": 1, "deaths": False},
        "Reaper": {"kills": 1, "assists": 1, "deaths": True},
    },
]

jugadores = {
    nombre: {"kills": 0, "assists": 0, "deaths": 0, "MVPs": 0, "points": 0}
    for nombre in rounds[0].keys()
}

for i in range(len(rounds) - 1):
    print(f"-Ranking ronda {i + 1}:")
    procesar(rounds[i], jugadores)
    imprimir(ordenar(jugadores))
print("-Ranking final: ")
procesar(rounds[i + 1], jugadores)
imprimir(ordenar(jugadores))
