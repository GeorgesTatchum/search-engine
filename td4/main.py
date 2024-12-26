import os
import sys

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re

from td3.td3 import load_docs
from td4.Author import Author
from td4.Corpus import SingletonCorpus
from td4.Document import Document

id2aut = {}
collection = {}
start_index_collection = 0


def convert_to_list(input_string: str) -> list:
    # Supprimer les crochets extérieurs et diviser par les accolades
    items = input_string.strip("[]").split("}, {")

    result = []
    for item in items:
        # Nettoyer chaque élément
        item = item.strip("{}")
        # Extraire le nom
        name = item.split(":")[1].strip().strip("'")
        result.append(name)

    return result


def add_to_id2aut(title: str, author: str) -> None:
    print(f"keys: {list(id2aut.keys())}")
    if str(author).lower() not in list(id2aut.keys()):
        print("id2aut is empty")
        auth = Author(str(author).lower())
        auth.add(title)
        id2aut[str(author).lower()] = auth
    else:
        print(f"auth: {author}")
        id2aut[str(author).lower()].add(title)


def init_corpus(collection: dict, id2aut: dict) -> SingletonCorpus:
    corpus = SingletonCorpus.get_instance()
    corpus.id2doc = collection
    corpus.authors = id2aut
    corpus.ndoc = len(collection)
    corpus.naut = len(id2aut)
    return corpus


def split_paragraph_into_sentences(paragraph: str) -> list:
    # Utiliser une expression régulière pour découper le paragraphe en phrases (en utilisant . et ? comme délimiteurs)
    sentence_endings = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
    sentences = sentence_endings.split(paragraph)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


if __name__ == "__main__":
    data = load_docs()
    print(data.info())
    for author, origin, title, date, text, url in data[
        ["author", "origin", "title", "date", "text", "url"]
    ].values:
        collection[str(start_index_collection)] = Document(
            titre=title,
            auteur=author,
            date=date,
            url=url,
            texte=text,
            type=origin.upper(),
        )
        # collection[str(start_index_collection)] = DocumentFactory.create_document(
        #     doc_type=origin.lower(),
        #     titre=title,
        #     auteur=author,
        #     date=date,
        #     url=url,
        #     texte=text,
        # )
        start_index_collection += 1
        if origin == "reddit":
            add_to_id2aut(title=title, author=author)
        if origin == "arxiv":
            list_authors = convert_to_list(author)
            for l_auth in list_authors:
                print(f"l_auth: {l_auth}")
                add_to_id2aut(title=title, author=l_auth)

    print(len(id2aut))
    print(len(collection))

    corpus = init_corpus(collection, id2aut)

    print("the corps is:", corpus)
