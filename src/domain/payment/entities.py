import uuid
from datetime import datetime

class PaymentTransaction:

    def __init__(self, amount: float, description: str):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.description = description
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"<Transaction {self.id} - {self.amount:.2f} EUR - {self.description} at {self.timestamp}>"
