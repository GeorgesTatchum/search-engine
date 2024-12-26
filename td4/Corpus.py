import re

import pandas as pd

from td4.Author import Author


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def _build_full_text(self):
        self._full_text = " ".join(doc.texte for doc in self.id2doc.values())

    def search(self, keyword):
        if not hasattr(self, "_full_text") or self._full_text is None:
            self._build_full_text()
        return re.findall(rf"\b{re.escape(keyword)}\b", self._full_text)

    def concorde(self, motif, taille_contexte=5):
        if not hasattr(self, "_full_text") or self._full_text is None:
            self._build_full_text()

        resultats = []
        for match in re.finditer(rf"\b{re.escape(motif)}\b", self._full_text):
            debut = max(0, match.start() - taille_contexte)
            fin = min(len(self._full_text), match.end() + taille_contexte)
            contexte_gauche = self._full_text[debut : match.start()]
            contexte_droit = self._full_text[match.end() : fin]
            resultats.append(
                {
                    "contexte gauche": contexte_gauche,
                    "motif trouvé": match.group(),
                    "contexte droit": contexte_droit,
                }
            )

        return pd.DataFrame(resultats)


class SingletonCorpus(Corpus):
    _instance = None

    @staticmethod
    def get_instance(nom="DefaultCorpus"):
        if SingletonCorpus._instance is None:
            SingletonCorpus._instance = SingletonCorpus(nom)
        return SingletonCorpus._instance

    def __init__(self, nom):
        if SingletonCorpus._instance is not None:
            raise Exception("This class is a singleton!")
        super().__init__(nom)
