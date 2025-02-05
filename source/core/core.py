from datetime import datetime as dt
from decimal import Decimal
from enum import StrEnum
from .Produit import ProduitData
import sqlite3
import sys


class MethodesPayment(StrEnum):
    CB = "CB"
    Cash = "Cash"


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

def generate_csv(dates: list[str]):
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    produits_list = get_produit()
    id_produit_map = {}
    for produit in produits_list:
        id_produit_map[produit.id_produit] = produit
    
    try:
        curseur = connection.cursor()
        
        requete = f"""
        SELECT id_produit, quantite FROM CommandeDetails 
        INNER JOIN Commande ON CommandeDetails.id_commande = Commande.id_commande 
        WHERE date=\"{"\" OR date=\"".join(dates)}\";
        """
        commandes = curseur.execute(requete).fetchall()

        data = [
            ["Produits", "Prix", "Quantités", "Totaux", "Total hebdomadaire"],
        ]

        produits_quantite = {}
        for commande in commandes:
            if commande[0] in produits_quantite:
                produits_quantite[commande[0]] += commande[1]
            else:
                produits_quantite[commande[0]] = commande[1]
        
        total_general = Decimal()
        for id_produit, quantite in produits_quantite.items():
            produit: ProduitData = id_produit_map[id_produit]
            total = produit.prix * quantite
            total_general += total
            
            data.append([produit.nom, produit.prix, quantite, total, None])

        data.append([None, None, None, None, total_general])
        
        return data
    except Exception as e:
        print(e)
    finally:
        connection.close()


def enregistrer_commande(methode: MethodesPayment, 
                        montant: Decimal, 
                        produits: dict[ProduitData: int]) -> None:
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
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    # 01/01/2020
    date = dt.today().strftime("%d/%m/%Y")
    # 13:05
    heure = dt.now().strftime("%H:%M")
    try:
        curseur = connection.cursor()
        curseur.execute(f"""INSERT INTO Commande (date, heure, total) VALUES ("{date}", "{heure}", "{montant}")""")
        id_commande = curseur.execute("SELECT MAX(Commande.id_commande) FROM Commande").fetchall()[0][0]
        
        for produit, quantite in produits.items():
            curseur.execute(f"""INSERT INTO CommandeDetails (id_commande, id_produit, quantite) VALUES ("{id_commande}", "{produit.id_produit}", "{quantite}")""")

        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()
    