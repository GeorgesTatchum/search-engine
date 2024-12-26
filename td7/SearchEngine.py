import os
import sys

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from td4.main import corpus


class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = {}
        self.num_docs = len(corpus.id2doc)
        self._build_vocab()
        self._build_tf_matrix()
        self._build_tfidf_matrix()

    def _build_vocab(self):
        all_docs_string = " ".join([x.texte for x in self.corpus.id2doc.values()])
        # découpage en mot (tri alphabétique et suppression de doublon)
        all_docs_string = sorted(set(all_docs_string.lower().split()))

        for index, value in enumerate(all_docs_string):
            self.vocab[value] = {"id": index, "nbr_occur": 0}

    def _build_tf_matrix(self):
        num_words = len(self.vocab)
        data, rows, cols = [], [], []

        for doc_id, doc in enumerate(self.corpus.id2doc.values()):
            word_counts = {}
            for word in doc.texte.lower().split():
                if word in self.vocab:
                    word_id = self.vocab[word]["id"]
                    if word_id not in word_counts:
                        word_counts[word_id] = 0
                    word_counts[word_id] += 1

            for word_id, count in word_counts.items():
                rows.append(doc_id)
                cols.append(word_id)
                data.append(count)

        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(self.num_docs, num_words))

        for word, info in self.vocab.items():
            word_id = info["id"]
            total_occurrences = self.mat_TF[:, word_id].sum()
            doc_frequency = (self.mat_TF[:, word_id] > 0).sum()
            self.vocab[word]["nbr_occur"] = total_occurrences
            self.vocab[word]["doc_freq"] = doc_frequency

    def _build_tfidf_matrix(self):
        tfidf_transformer = TfidfTransformer()
        self.mat_TF_IDF = tfidf_transformer.fit_transform(self.mat_TF)
        self.tfidf_transformer = tfidf_transformer

    def search(self, query, top_n=5):
        # Transformer ces mots-clefs sous la forme d'un vecteur sur le vocabulaire précédemment construit
        query_vector = np.zeros((1, len(self.vocab)))
        for word in query.lower().split():
            if word in self.vocab:
                word_id = self.vocab[word]["id"]
                query_vector[0, word_id] += 1

        # Calculer la similarité entre le vecteur requête et tous les documents
        query_tfidf = self.tfidf_transformer.transform(query_vector)
        similarities = cosine_similarity(query_tfidf, self.mat_TF_IDF).flatten()

        # Trier les scores résultats et afficher les meilleurs résultats
        sorted_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in sorted_indices[:top_n]:
            results.append({"Document ID": idx, "Similarité": similarities[idx]})

        return pd.DataFrame(results)


search_engine = SearchEngine(corpus)
result_df = search_engine.search("covid9", top_n=5)
print(result_df)
