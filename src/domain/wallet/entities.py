# src/domain/wallet/entities.py

from domain.wallet.value_objects import Amount

class Wallet:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.balance = 0.0  # in EUR

    def deposit(self, amount: Amount):
        if amount.value <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount.to_euro().value

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        return round(self.balance, 2)
