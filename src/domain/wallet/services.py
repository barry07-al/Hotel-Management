from domain.wallet.entities import Wallet
from domain.wallet.repository import WalletRepository
from domain.wallet.value_objects import Amount

class WalletService:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    def deposit(self, user_id: str, amount: Amount):
        wallet = self.wallet_repo.get_by_user_id(user_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        wallet.deposit(amount)
        self.wallet_repo.save(wallet)

    def withdraw(self, user_id: str, amount: float):
        wallet = self.wallet_repo.get_by_user_id(user_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        wallet.withdraw(amount)
        self.wallet_repo.save(wallet)

    def get_balance(self, user_id: str) -> float:
        wallet = self.wallet_repo.get_by_user_id(user_id)
        if not wallet:
            raise ValueError("Wallet not found.")
        return wallet.get_balance()
