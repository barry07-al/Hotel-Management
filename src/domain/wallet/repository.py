from domain.wallet.entities import Wallet

class WalletRepository:

    def __init__(self):
        self._storage = {}  # user_id -> Wallet

    def save(self, wallet: Wallet, user_id: str = None):
        uid = user_id or getattr(wallet, "user_id", None)
        if not uid:
            raise ValueError("Wallet must be associated with a user_id")
        wallet.user_id = uid  # attach ID if needed
        self._storage[uid] = wallet

    def get_by_user_id(self, user_id: str) -> Wallet | None:
        return self._storage.get(user_id)

    def get_all(self) -> list[Wallet]:
        return list(self._storage.values())
