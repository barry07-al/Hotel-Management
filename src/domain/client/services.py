from .entities import Client
from .repository import ClientRepository
from .value_objects import FullName, Email, PhoneNumber


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def register_client(self, first_name: str, last_name: str, email: str, phone_number: str) -> Client:
        full_name_vo = FullName(first_name, last_name)
        email_vo = Email(email)
        phone_vo = PhoneNumber(phone_number)
        if self.repository.get_by_email(email_vo):
            raise ValueError("A client with this email already exists.")
        client = Client(full_name=full_name_vo, email=email_vo, phone_number=phone_vo)
        self.repository.save(client)
        return client

    def get_client_by_id(self, client_id: str) -> Client | None:
        return self.repository.get_by_id(client_id)

    def get_all_clients(self) -> list[Client]:
        return self.repository.get_all()
