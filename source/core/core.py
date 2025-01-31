from datetime import datetime as dt
from decimal import Decimal
from PySide6.QtGui import QPdfWriter
import json as js
from decimal import Decimal, getcontext

class Core(object):
    def __init__(self):
        super().__init__(self)
        # super().float_to_decimal()

    def float_to_decimal(number:float) -> Decimal:
        getcontext().prec = 28#number of rounding point
        return Decimal(number)

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

    def pdfPayment (self, name: str|None = None, datedebut: dt = dt.today(), datefin: dt = dt.today()):
        # if (name == None):
        #     name = "{datedebut} to {datefin}"

        # json_data = js.load("Payment.json")

        # doc = pdf.Document()
        # page:pdf.Document.pages = doc.pages.add()

        # currentdate = datedebut
        # while (currentdate <= datedebut):
        #     jsondatedata: list[Decimal, list[list[str, str, Decimal, dt, list[str]]]]|None = json_data[currentdate]

        #     if not jsondatedata:
        #         text = pdf.TeXFragment("{currentdate}:\n\tNo Record")
        #     else:
        #         text = pdf.TeXFragment("""{currentdate}:
        #                                     Montant des achats: {jsondatedata[0]}
        #                                     {printable(jsondatedata[1])}""")
        # page.paragraphs.add(text)
        pass
