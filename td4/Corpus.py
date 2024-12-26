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

    def nettoyer_texte(self, texte):
        # Mise en minuscules
        texte = texte.lower()
        # Remplacement des passages à la ligne
        texte = texte.replace("\n", " ")
        # Suppression de la ponctuation et des chiffres
        texte = re.sub(r"[^\w\s]", "", texte)
        texte = re.sub(r"\d+", "", texte)
        return texte

    def construire_vocabulaire(self):
        vocabulaire = set()
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = re.split(r"\s+", texte_nettoye)
            vocabulaire.update(mots)
        return {mot: 0 for mot in vocabulaire if mot}  # Exclure les chaînes vides

    def compter_occurrences(self):
        vocabulaire = self.construire_vocabulaire()
        doc_freq = {mot: 0 for mot in vocabulaire}

        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = re.split(r"\s+", texte_nettoye)
            mots_uniques = set(mots)
            for mot in mots:
                if mot in vocabulaire:
                    vocabulaire[mot] += 1
            for mot in mots_uniques:
                if mot in doc_freq:
                    doc_freq[mot] += 1

        freq_df = pd.DataFrame(
            {
                "mot": vocabulaire.keys(),
                "frequence": vocabulaire.values(),
                "doc_frequency": [doc_freq[mot] for mot in vocabulaire],
            }
        )
        freq_df = freq_df.sort_values("frequence", ascending=False).reset_index(
            drop=True
        )
        return freq_df

    def stats(self, n=10):
        freq_df = self.compter_occurrences()
        nb_mots_differents = len(freq_df)

        print(f"Nombre de mots différents dans le corpus : {nb_mots_differents}")
        print(f"\n{n} mots les plus fréquents :")
        print(freq_df.head(n).to_string(index=False))


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
