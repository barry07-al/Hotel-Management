from domain.wallet.value_objects import Amount
from domain.wallet.repository import WalletRepository

class WalletService:

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    def deposit(self, client_id: str, amount: Amount):
        wallet = self.wallet_repo.get_by_client_id(client_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        wallet.deposit(amount)
        self.wallet_repo.save(wallet)

    def withdraw(self, client_id: str, amount: float):
        wallet = self.wallet_repo.get_by_client_id(client_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        wallet.withdraw(amount)
        self.wallet_repo.save(wallet)

    def get_balance(self, client_id: str) -> float:
        wallet = self.wallet_repo.get_by_client_id(client_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        return wallet.get_balance()
