import json
import os
import urllib.request
from datetime import datetime

import pandas as pd
import praw
import xmltodict

# Partie 1 : chargement des données

# REDDIT


def get_reddit_data(search_query: str) -> None:
    """Récupère les données de Reddit et les sauvegarde dans un fichier JSON"""
    reddit = praw.Reddit(
        client_id="KTdgvYo7sGyiNb02hQZWJQ",
        client_secret="wTyymqM0ysjUrLrK7nkLMZHwq1ERlg",
        user_agent="ferdaousse",
    )
    posts = reddit.subreddit(search_query).hot(limit=100)
    textes_reddit = []

    for i, post in enumerate(posts):
        if post.selftext != "":
            textes_reddit.append(
                {
                    "origin": "reddit",
                    "title": str(post.title),
                    "author": str(post.author.name),
                    "date": datetime.utcfromtimestamp(post.created_utc).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "url": str(post.url),
                    "text": str(post.selftext.replace("\n", " ")),
                }
            )
    with open("td3/textes.json", "w", encoding="utf-8") as f:
        json.dump(textes_reddit, f, ensure_ascii=True, indent=4)


def get_arxiv_data(query_terms: list[str], limit: int) -> None:
    """Récupère les données de Arxiv et les sauvegarde dans un fichier JSON"""
    textes_Arvix = []

    url = f"http://export.arxiv.org/api/query?search_query=all:{query_terms[0]}&start=0&max_results={limit}"
    entries = urllib.request.urlopen(url)
    data = xmltodict.parse(entries.read().decode("utf-8"))

    for i, entry in enumerate(data["feed"]["entry"]):
        if entry["summary"] != "":
            textes_Arvix.append(
                {
                    "origin": "arxiv",
                    "title": str(entry["title"]),
                    "author": str(entry["author"]),
                    "date": datetime.strptime(
                        entry["published"], "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "url": str(entry["id"]),
                    "text": str(entry["summary"].replace("\n", " ")),
                }
            )

    try:
        with open("td3/textes.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(textes_Arvix)
    # Écrire la liste mise à jour dans le fichier JSON
    with open("td3/textes.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=True, indent=4)


def create_dataframe_from_json(json_file: str) -> pd.DataFrame:
    json_file = os.path.abspath(json_file)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

        df = pd.DataFrame(
            data, columns=["origin", "title", "author", "date", "url", "text"]
        )

        df["origin"] = df["origin"].astype(str)
        df["title"] = df["title"].astype(str)
        df["author"] = df["author"].astype(str)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
        df["url"] = df["url"].astype(str)
        df["text"] = df["text"].astype(str)

        df.reset_index(inplace=True)
        df.rename(columns={"index": "id"}, inplace=True)

        return df


def load_docs() -> pd.DataFrame:
    """Charge les données à partir d'un fichier CSV"""
    if os.path.exists("td3/dtextes.csv"):
        return pd.read_csv("td3/dtextes.csv")
    else:
        print("dtextes.csv does not exist in the current directory.")
        return None


def create_single_string_from_docs(df: pd.DataFrame) -> str:
    """Crée une unique chaîne de caractères contenant tous les documents"""
    return " ".join(df["text"].tolist())


if __name__ == "__main__":
    # print("xxxx")
    # get_reddit_data(search_query="Coronavirus")
    # get_arxiv_data(query_terms=["Coronavirus"], limit=100)
    # print("yyyyyy")

    df = create_dataframe_from_json("td3/textes.json")
    df.to_csv("td3/dtextes.csv", index=False)
    print(df.info())

# print(f"tailles des données: {df.shape}")

# # Supprimer les documents trop petits (moins de 20 caractères)
# df = df[df["text"].apply(lambda x: len(x) >= 20)].reset_index(drop=True)

# # Créer une unique chaîne de caractères contenant tous les documents
# all_docs_string = create_single_string_from_docs(df)
# print(all_docs_string)
# with open("td3/textes_long.json", "w", encoding="utf-8") as f:
#     json.dump(all_docs_string, f, ensure_ascii=True, indent=4)

# for i, doc in enumerate(df["text"]):
#     phrases = doc.split(".")
#     print(f"nombre de phrases dans le document d'indice {i}: {len(phrases)}")
#     for num, phrase in enumerate(phrases):
#         print(
#             f"nombre de mots dans la phrase {num}, du doc numero {i} : {len(phrase.split())}"
#         )
#         print("*************")
