from domain.wallet.value_objects import Amount
from application.exceptions import ApplicationError

class Wallet:

    def __init__(self, client_id: str):
        self.balance = 0.0
        self.client_id = client_id

    def deposit(self, amount: Amount):
        if amount.value <= 0:
            raise ApplicationError("Deposit amount must be positive.")
        self.balance += amount.to_euro().value

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ApplicationError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ApplicationError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        return round(self.balance, 2)
