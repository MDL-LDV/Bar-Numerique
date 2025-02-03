import datetime as dt
from dataclasses import dataclass
from decimal import Decimal, getcontext

@dataclass
class DataCore:
    """
    Purpose: defying the properties in use in the main class
    """

    today: str = dt.datetime.today().strftime("%d%m%Y")
    money: float = 0
    # payment: list[str] = ["CB", "cash"]
    # itemVendu: list[str] = ["Cappuccino", "Café", "1/2 Café", "Chocolat Chaud",
    #                         "Thé", "Jus de Pomme", "Grand Sirop", "Sirop"]

    def float_to_decimal(number:float) -> Decimal:
        getcontext().prec = 28#number of rounding point
        return Decimal(number)