from domain.wallet.entities import Wallet
from application.exceptions import ApplicationError

class WalletRepository:

    def __init__(self):
        self._storage = {}

    def save(self, wallet: Wallet, client_id: str = None):
        uid = client_id or getattr(wallet, "client_id", None)
        if not uid:
            raise ApplicationError("Wallet must be associated with a client ID.")
        wallet.client_id = uid
        self._storage[uid] = wallet

    def get_by_client_id(self, client_id: str) -> Wallet | None:
        res = self._storage.get(client_id, False)
        if not res:
            raise ApplicationError(f"Wallet not found for client {client_id}.")
        return res

    def get_all(self) -> list[Wallet]:
        return list(self._storage.values())
