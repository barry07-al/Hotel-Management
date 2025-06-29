import uuid

from datetime import datetime

from application.exceptions import ApplicationError

class PaymentTransaction:

    def __init__(self, amount: float, description: str):
        if amount <= 0:
            raise ApplicationError("Transaction amount must be positive.")
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.description = description
        self.timestamp = datetime.now()

