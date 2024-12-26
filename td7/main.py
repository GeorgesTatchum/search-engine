import os
import sys

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from td4.main import corpus

# == Partie 1


all_docs_string = " ".join([x.texte for x in corpus.id2doc.values()])

print(f"the textes : {all_docs_string}")


# découpage en mot (tri alphabétique et suppression de doublon)
all_docs_string = sorted(set(all_docs_string.lower().split()))

vocab = {}
for index, value in enumerate(all_docs_string):
    vocab[value] = {"id": index, "nbr_occur": 0}

print(f"the vocab : {vocab}")
# Initialisation des valeurs de la matrice
num_docs = len(corpus.id2doc)
num_words = len(vocab)
data = []
rows = []
cols = []

# construction de la matrice
for doc_id, doc in enumerate(corpus.id2doc.values()):
    word_counts = {}
    for word in doc.texte.lower().split():
        if word in vocab:
            word_id = vocab[word]["id"]
            if word_id not in word_counts:
                word_counts[word_id] = 0
            word_counts[word_id] += 1

    for word_id, count in word_counts.items():
        rows.append(doc_id)
        cols.append(word_id)
        data.append(count)


mat_TF = csr_matrix((data, (rows, cols)), shape=(num_docs, num_words))

print(mat_TF)

# Calcul du total d'occurance et de la fréquence
for word, info in vocab.items():
    word_id = info["id"]
    # total d'occurance du mot dans le corpus
    total_occurrences = mat_TF[:, word_id].sum()
    # Nombre de document contenant le mot
    doc_frequency = (mat_TF[:, word_id] > 0).sum()

    vocab[word]["nbr_occur"] = total_occurrences
    vocab[word]["doc_freq"] = doc_frequency

print(
    f"Mise à jour du vocabulaire avec occurrences et fréquences des documents: {vocab}"
)

# Calcul de la matrice TF-IDF

# Initialisation du transformateur TF-IDF
tfidf_transformer = TfidfTransformer()

# Calcul de la matrice TF-IDF à partir de la matrice TF
mat_TF_IDF = tfidf_transformer.fit_transform(mat_TF)

print(f" matrice tf-idf : {mat_TF_IDF}")

# == Partie 2
# Demander à l'utilisateur d'entrer quelques mots-clefs
query = input("Entrez quelques mots-clefs: ").lower().split()

# Transformer ces mots-clefs sous la forme d'un vecteur sur le vocabulaire précédemment construit
query_vector = np.zeros((1, num_words))
for word in query:
    if word in vocab:
        word_id = vocab[word]["id"]
        query_vector[0, word_id] += 1

# Calculer la similarité entre le vecteur requête et tous les documents
query_tfidf = tfidf_transformer.transform(query_vector)
similarities = cosine_similarity(query_tfidf, mat_TF_IDF).flatten()

# Trier les scores résultats et afficher les meilleurs résultats
sorted_indices = np.argsort(similarities)[::-1]
top_n = 5  # Nombre de résultats à afficher
for idx in sorted_indices[:top_n]:
    print(f"Document ID: {idx}, Similarité: {similarities[idx]}")
