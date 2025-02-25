from datetime import datetime as dt
from decimal import Decimal
from enum import StrEnum
from .Produit import ProduitData, CommandeData
import sqlite3
import sys

from typing import Optional


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


def concatenation(
        main_liste: list, 
        args: tuple[dict], 
        conv: tuple[callable], 
        extract_function: callable = None):
    result = []
    
    for value in main_liste:
        if extract_function:
            key = extract_function(value)
        else:
            key = value

        row = [key]

        for i, d in enumerate(args):
            if conv[i] is not None:
                row.append(conv[i](d[key]))
            else:
                row.append(d[key])
            
        result.append(row)

    return result


def generate_csv(dates: list[str]):
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    produits = get_produit()
    
    table = []
    
    try:
        curseur = connection.cursor()
        
        requete = f"""
        SELECT Produit.nom, Produit.prix, CommandeDetails.quantite 
        FROM CommandeDetails 
        INNER JOIN Commande ON 
            CommandeDetails.id_commande = Commande.id_commande
        INNER JOIN Produit ON 
            CommandeDetails.id_produit = Produit.id_produit
        WHERE (date={" OR date=".join(dates)})
        """

        for m in list(MethodesPayment):
            methode = str(m)

            requete_methode = requete + f" AND methode=\"{methode}\";"
            commandes = curseur.execute(requete_methode).fetchall()
            table_part = [
                [methode, None, None, None, None],
                ["Produits", "Prix", "Quantités", "Totaux", "Total hebdomadaire"],
            ]
            produits_quantite = {}
            produit_total = {}
            produit_prix = {}
            empty_row = {}
            total_general = Decimal()

            for commande in commandes:
                nom = commande[0]
                prix = Decimal(commande[1])
                quantite = int(commande[2])
                if commande[0] in produits_quantite:
                    produits_quantite[nom] += quantite
                    produit_total[nom] += prix * quantite
                else:
                    produits_quantite[nom] = quantite
                    produit_total[nom] = prix * quantite
                
                total_general += prix * quantite
            
            for produit in produits:
                if produit.nom not in produits_quantite:
                    produits_quantite[produit.nom] = 0
                    produit_total[produit.nom] = Decimal()
                
                produit_prix[produit.nom] = produit.prix
                empty_row[produit.nom] = None
            
            data = concatenation(
                produits, 
                (produit_prix, produits_quantite, produit_total, empty_row), 
                (lambda v: str(v), None, lambda v: str(v), None),
                extract_function=lambda p: p.nom)

            data = sorted(data, key=lambda t: t[0])

            table_part.extend(data)
            
            table_part.append([None, None, None, None, str(total_general)])
            table_part.append([None, None, None, None, None])

            table.extend(table_part)
        return table
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
    # 31/12/2020 -> 20201231
    date = dt.today().strftime("%Y%m%d")
    date = int(date)
    # 13:05
    heure = dt.now().strftime("%H%M")
    heure = int(heure)
    try:
        curseur = connection.cursor()
        curseur.execute(f"""INSERT INTO Commande (date, heure, total, methode) VALUES ("{date}", "{heure}", "{montant}", "{str(methode)}")""")
        id_commande = curseur.execute("SELECT MAX(Commande.id_commande) FROM Commande").fetchall()[0][0]
        
        for produit, quantite in produits.items():
            curseur.execute(f"""INSERT INTO CommandeDetails (id_commande, id_produit, quantite) VALUES ("{id_commande}", "{produit.id_produit}", "{quantite}")""")

        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


def get_commande(
        debut: Optional[int] = None, 
        fin: Optional[int] = None) -> list[CommandeData]:
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    curseur = connection.cursor()
    requete = "SELECT * FROM Commande"
    if debut and fin:
        requete += f" WHERE date >= {debut} AND date <= {fin}"
    data = curseur.execute(requete).fetchall()
    connection.close()

    commande_list = []
    for row in data:
        data_dict = {key: row[i] for i, key in enumerate(CommandeData.model_fields.keys())}
        commande_list.append(CommandeData.model_validate(data_dict))

    return commande_list


def delete_commande(id_commande: int) -> None:
    connection = sqlite3.connect(sys.path[0] + "\\commandes.sqlite3")
    curseur = connection.cursor()

    try:
        curseur.execute(f"DELETE FROM CommandeDetails WHERE id_commande={id_commande}")
        curseur.execute(f"DELETE FROM Commande WHERE id_commande={id_commande}")

        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()
