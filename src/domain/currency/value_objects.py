from enum import Enum

class Currency(Enum):
    EUR = "Euro"
    USD = "Dollar"
    GBP = "Pound Sterling"
    JPY = "Yen"
    CHF = "Swiss Franc"

    def __str__(self):
        return self.name
