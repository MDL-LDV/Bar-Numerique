from datetime import datetime as dt
from decimal import Decimal
from enum import StrEnum
from .Produit import ProduitData
from pydantic import BaseModel, Field, ConfigDict
import sqlite3
import sys


class MethodesPayment(StrEnum):
    CB = "CB"
    Cash = "Cash"


class Commande(BaseModel):
    # Forbid extra arguments and freeze the data to make it hashable (dict)
    model_config = ConfigDict(extra='forbid', frozen=True)

    methode_payment: MethodesPayment = Field(..., frozen=True)
    montant: Decimal = Field(..., frozen=True)
    produits: list[ProduitData] = Field(..., frozen=True)


def get_produit() -> list[ProduitData]:
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    curseur = connection.cursor()
    data = curseur.execute("SELECT * FROM Produit").fetchall()
    connection.close()

    produit_list = []
    for row in data:
        data_dict = {key: row[i] for i, key in enumerate(ProduitData.model_fields.keys())}
        produit_list.append(ProduitData.model_validate(data_dict))

    return produit_list

def enregistrer_commande(methode: MethodesPayment, 
                        montant: Decimal, 
                        produits: list[ProduitData]) -> None:
    """
    Entrées:
        methode: PaymentMethod
        montant: Decimal
        produits: list[ProduitData]
    Sortie:
        None (modification de fichier)
    Rôle:
        Enregistre la commande dans un
    """
    def parse_list(liste) -> dict[ProduitData: int]:
        dictionnaire = {}
        for element in liste:
            if element in dictionnaire:
                dictionnaire[element] += 1
            else:
                dictionnaire[element] = 1
                
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    date = dt.today().strftime("%d/%m/%Y")
    heure = dt.now().strftime("%H:%M")
    try:
        curseur = connection.cursor()
        curseur.execute(f"""INSERT INTO Commande (date, heure, total) VALUES ("{date}", "{heure}", "{montant}")""")
        id_commande = curseur.execute("SELECT MAX(Commande.id_commande) FROM Commande").fetchall()
        print(id_commande)
        produits: dict[ProduitData: int] = parse_list(produits)
        
        for produit, quantite in produit.items():
            curseur.execute(f"""INSERT INTO CommandeDetails (id_commande, id_produit, quantite) VALUES ("{id_commande}", "{produit.id_produit}", "{quantite}")""")

        # curseur.execute(f"""INSERT INTO CommandeDetails (date, heure, total) VALUES ("{date}", "{heure}", "{montant}")""")
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()
    