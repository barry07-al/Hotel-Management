from infrastructure.persistence import Persistence
from domain.payment.entities import PaymentTransaction

class PaymentRepository:
    def __init__(self):
        self._transactions: list[PaymentTransaction] = Persistence.load_transactions()

    def record(self, transaction: PaymentTransaction):
        self._transactions.append(transaction)
        Persistence.save_transactions(self._transactions)

    def get_all(self) -> list[PaymentTransaction]:
        return self._transactions
