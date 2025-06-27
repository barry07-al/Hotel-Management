from domain.currency.value_objects import Currency
from application.exceptions import ApplicationError

class Amount:
    exchange_rates = {
        Currency.EUR: 1.0,
        Currency.USD: 0.93,
        Currency.GBP: 1.17,
        Currency.JPY: 0.0060,
        Currency.CHF: 1.02
    }

    def __init__(self, value: float, currency: Currency):
        if value <= 0:
            raise ApplicationError("Amount must be positive.")
        if currency not in self.exchange_rates:
            raise ApplicationError(f"Unsupported currency: {currency}")
        self.value = value
        self.currency = currency

    def to_euro(self) -> 'Amount':
        euro_value = self.value * self.exchange_rates[self.currency]
        return Amount(euro_value, Currency.EUR)
