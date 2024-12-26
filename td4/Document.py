class Document:
    def __init__(self, titre, auteur, date, url, texte, type):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    def __str__(self):
        return f"{self.titre}, par {self.auteur}"


class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte):
        type = "reddit"
        super().__init__(self, titre, auteur, date, url, texte, type)
        self.nbr_commentaires = 0

    def __str__(self):
        return f"{super().__str__()}, (Reddit) - {self.nbr_commentaires} commentaires"

    def get_nbr_commentaires(self) -> int:
        return self.nbr_commentaires

    def set_nbr_commentaires(self, nbr: int) -> None:
        self.nbr_commentaires = nbr

    def getType(self):
        return str(self.type).upper()


class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte):
        type = "arxiv"
        super().__init__(titre, auteur, date, url, texte, type)
        self.co_auteurs = []

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def __str__(self):
        co_authors_str = ", ".join(self.co_auteurs)
        return f"{super().__str__()} (Arxiv) - Co-auteurs: {co_authors_str}"

    def getType(self):
        return str(self.type).upper()


class DocumentFactory:
    @staticmethod
    def create_document(doc_type, **kwargs):
        if doc_type == "reddit":
            return RedditDocument(**kwargs)
        elif doc_type == "arxiv":
            return ArxivDocument(**kwargs)
        else:
            raise ValueError("Unknown document type")
