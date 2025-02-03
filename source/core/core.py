from Helper import DataCore
from datetime import datetime as dt
from decimal import Decimal
import json as js
import csv

class Core(DataCore):
    def __init__(self):
        super().__init__(self)


    def add_payment_to_json(self, method: str, montant: float, itemVendu: list[str], name: str = "nobody"):
        if (method in self.payment):
            data = js.load("Payment.json")
            if (dt.today() in data):
                currentdata = data[dt.today()]
                Moneypayment: Decimal = self.float_to_decimal(montant)
                currentdata["amount"] += Moneypayment
                currentdata["payment"].append([
                    name,
                    method,
                    Moneypayment,
                    dt.now(),
                    itemVendu
                    ])
            else:
                Moneypayment: Decimal = self.float_to_decimal(montant)
                data[dt.today()]["amount"] = self.float_to_decimal(montant) 
                data[dt.today()]["payment"].append([
                    name,
                    method,
                    Moneypayment,
                    dt.now(),
                    itemVendu
                ])
        else:
            raise "Unknown method of payment"

    def JsonToCSV (self, name: str, datedebut: dt = dt.today(), datefin: dt = dt.today()):       
        json_data = js.load("Payment.json")

        with open(name, "w+") as file:
            writer = csv.writer(file)
            writer.writerows(
                    ["Produits", "Prix", "Quantités", "Totaux", "Total hebdomadaire"],
                    ["Cappuccino", 0.40, 0, 0, 0],
                    ["Café", 0.40, 0, 0, 0],
                    ["1/2 Café", 0.20, 0, 0, 0],
                    ["Chocolat Chaud", 0.40, 0, 0, 0],
                    ["Thé", 0.15, 0, 0, 0],
                    ["Jus de Pomme", 0.40, 0, 0, 0],
                    ["Grand Sirop", 0.30, 0, 0, 0],
                    ["Sirop", 0.10, 0, 0, 0]
                    ["", "", "", "", 0]
                )

            currentdate = datedebut
            while (currentdate <= datedebut):
                jsondatedata: list[Decimal, list[list[str, str, Decimal, dt, list[str]]]]|None = json_data[currentdate]
                
                
            
    
    
                

        
            



    

    



