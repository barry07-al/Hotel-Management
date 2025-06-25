from domain.wallet.entities import Wallet

class WalletRepository:

    def __init__(self):
        self._storage = {}

    def save(self, wallet: Wallet, client_id: str = None):
        uid = client_id or getattr(wallet, "client_id", None)
        if not uid:
            raise ValueError("Wallet must be associated with a client ID.")
        wallet.client_id = uid
        self._storage[uid] = wallet

    def get_by_client_id(self, client_id: str) -> Wallet | None:
        return self._storage.get(client_id)

    def get_all(self) -> list[Wallet]:
        return list(self._storage.values())
