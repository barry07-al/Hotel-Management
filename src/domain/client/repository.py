from typing import Optional, List

from .entities import Client
from infrastructure.persistence import Persistence

class ClientRepository:

    def __init__(self, file_path: str = "data/clients.txt"):
        self.file_path = file_path
        self._storage = {client.id: client for client in Persistence.load_clients(file_path)}

    def save(self, client: Client):
        existing = self.get_by_email(client.email)
        if existing and existing.id != client.id:
            raise ValueError(f"Client with email {client.email.value} already exists.")
        self._storage[client.id] = client
        self._persist()

    def get_by_id(self, client_id: str) -> Optional[Client]:
        return self._storage.get(client_id)

    def get_by_email(self, email) -> Optional[Client]:
        for client in self._storage.values():
            if client.email == email:
                return client
        return None

    def get_all(self) -> List[Client]:
        return list(self._storage.values())

    def _persist(self):
        Persistence.save_clients(self.get_all(), self.file_path)
