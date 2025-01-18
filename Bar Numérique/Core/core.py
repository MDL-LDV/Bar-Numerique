import datetime as dt
import abc

class Truc:
    """
    Purpose: The main class that define the behaviour of the 
    """
   
    def __init__(self):
        self.date = dt.datetime.today()
        self.money: float = 0
        self.payment: str|None
        
    def __add__(self, left, right) -> int|float:
        if 
