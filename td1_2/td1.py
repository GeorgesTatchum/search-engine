import json

import pandas as pd

with open("evg_esp_veg.envpdiprboucle.json", "r") as f:
    d_json = json.load(f)
    var = d_json["fields"]
    rando = d_json["values"]
    print(var)
    print(rando)

    # taille des données
    print(len(rando))

    # nom à 10 ligne
    print(rando[9]["nom"])

    df = pd.DataFrame.from_dict(rando)

    print(f"the head: {df.head()} and tail: {df.tail()}")

    print(df["xdepart"].mean())
    print(f"the prev : {df['temps_parcours']}")
    df["temps_parcours"] = [int(x[:-3]) for x in df["temps_parcours"]]
    print(f"the curr : {df['temps_parcours']}")
    print(f"the temps_parcours mean : {df['temps_parcours'].mean()}")

    print(df.groupby(by="difficulte")["temps_parcours"].mean())

    print(df["difficulte"].sort_index(ascending=True).value_counts().plot.pie())
    # print(df["difficulte"].sort_index(ascending=True).value_counts().plot.bar())

    # plt.xlabel("Niveau de difficulté")
    # plt.ylabel("Nombre de randonnées")
    # plt.title("Nombre de randonnées par niveau de difficulté")
    # plt.show()

    # display the longueur column
    print(f"befor convertion : {df['longueur']}")
    df["longueur"] = [
        float(x[:-3].replace(",", ".")) if "," in x else float(x[:-3])
        for x in df["longueur"]
    ]
    print(f"after convertion : {df['longueur']}")

    print(f"check null value : {df.isnull().sum()}")

    # croisement des deux variables
    # df.plot.scatter(y="temps_parcours", x="longueur", c="#353DAB", s=50)

    # plt.ylabel("temps de parcours (min)")
    # plt.xlabel("longueur des randonnées (km)")
    # plt.title("croisement des variables")
    # plt.show()

    # Calculer la corrélation entre 'longueur' et 'temps_parcours'
    # correlation = df["longueur"].corr(df["temps_parcours"])
    correlation = df["longueur"].corr(df["temps_parcours"], method="kendall")

    # Afficher la corrélation
    print(f"Corrélation entre 'longueur' et 'temps_parcours' : {correlation}")

df_lieux = pd.read_csv("lieux-2018.csv", encoding="latin1")
df_vehicules = pd.read_csv("vehicules-2018.csv", encoding="latin1")
df_usagers = pd.read_csv("usagers-2018.csv", encoding="latin1")
df_caracteristiques = pd.read_csv("caracteristiques-2018.csv", encoding="latin1")

print(df_lieux.head())
print(df_vehicules.head())
print(df_usagers.head())
print(df_caracteristiques.head())

accidents_lyon = df_caracteristiques[df_caracteristiques["dep"] == "690"]

print(f"nombre d'accidents à Lyon : {(accidents_lyon.shape[0])}")

print(df_vehicules.info())

accidents_velo = df_vehicules[df_vehicules["catv"] == 1]

print(f"nombre d'accidents impliquant une bicyclette : {(accidents_velo.shape[0])}")

accidents_velos_lyon = accidents_lyon.join(accidents_velo, how="inner", lsuffix="_lyon")

print(accidents_velos_lyon)
