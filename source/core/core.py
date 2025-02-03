from Helper import DataCore
from datetime import datetime as dt
from decimal import Decimal
from win32con import GENERIC_WRITE, FILE_SHARE_WRITE
import win32print
import win32ui
import json as js
import csv
import os



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

    def JsonToCSV (self, filename: str, datedebut: dt = dt.today(), datefin: dt = dt.today()) -> bool:       
        """
        Entry:
            name: str
                Name of the file with the extension .csv
            datedebut: dt
                The record debut date that will be write on the file
            datefin:
                The record end date that will be write on the file

        Return:
            Bool:
                True:
                    the file as been created and fill
                False:
                    and error occured, idk

        Purpose:
            Take the Payment.json and convert all the data into an csv
        
        """
        json_data = js.load("Payment.json")

        Cappu:list[int, float] = []#[quantitié, total]
        cafe:list[int, float] = []
        demicafe:list[int, float] = []
        choc:list[int, float] = []
        The:list[int, float] = []
        Jus:list[int, float] = []
        GrandSirop:list[int, float] = []
        Sirop:list[int, float] = []


        currentdate = datedebut
        while (currentdate <= datedebut):
            jsondatedata: list[Decimal, list[list[str, str, Decimal, dt, list[str]]]]|None = json_data[currentdate]
                
            for command in jsondatedata[1]:
                for Nomproduit in command[4]:
                    match Nomproduit:
                        case "Cappuccino":
                            Cappu[0] += 1
                            Cappu[1] += 0.4
                            
                        case "Café":
                            cafe[0] += 1
                            cafe[1] += 0.4
                            
                        case "1/2 Café":
                            demicafe[0] += 1
                            demicafe[1] += 0.2

                        case "Chocolat Chaud":
                            choc[0] += 1
                            choc[1] += 0.4

                        case "Thé":
                            The[0] += 1
                            The[1] += 0.15

                        case "Jus de Pomme":
                            Jus[0] += 1
                            Jus[1] += 0.3
                            
                        case "Grand Sirop":
                            GrandSirop[0] += 1
                            GrandSirop[1] += 0.3

                        case "Sirop":
                            Sirop[0] += 1
                            Sirop[1] += 0.1
                        case _:
                            raise "Unknown product name {Nomproduit}"


        repr_debut = datedebut.day + r"/" + datedebut.month + r"/" + datedebut.year
        repr_fin = datefin.day + r"/" + datefin.month + r"/" + datefin.year

        with open(filename, "w+") as file:
            writer = csv.writer(file)

            
            writer.writerows(
                    ["Produits", "Prix", "Quantités", "Totaux", "resultat du {repr_debut} au {repr_fin}"],
                    ["Cappuccino", 0.40, Cappu[0], Cappu[1], ""],
                    ["Café", 0.40, cafe[0], cafe[1], ""],
                    ["1/2 Café", 0.20, demicafe[0], demicafe[1], ""],
                    ["Chocolat Chaud", 0.40, choc[0], choc[1], ""],
                    ["Thé", 0.15, The[0], The[1], ""],
                    ["Jus de Pomme", 0.30, Jus[0], Jus[1], ""],
                    ["Grand Sirop", 0.30, GrandSirop[0], GrandSirop[1], ""],
                    ["Sirop", 0.10, Sirop[0], Sirop[1], ""]
                    ["", "", "", "", jsondatedata[0]]
                )
            
    def ImpressFile(self, filename:str) -> bool|Exception:
        directory = os.getcwd()
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            printer_name = win32print.GetDefaultPrinter()
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
            # Start a print job
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Print Job", None, "RAW"))
                try:
                    # Start a print page
                    win32print.StartPagePrinter(hPrinter)
                    try:
                        # Write the file to the printer
                        with open(file_path, 'rb') as f:
                            win32print.WritePrinter(hPrinter, f.read())
                    finally:
                        win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
        return True


            
    
    
                

        
            



    

    



