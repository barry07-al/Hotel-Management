import unittest

from unittest.mock import MagicMock

from src.domain.client.entities import Client
from src.domain.client.services import ClientService


class TestClientService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock()
        self.service = ClientService(self.mock_repository)

    def test_register_client_success(self):
        self.mock_repository.get_by_email.return_value = None
        client = self.service.register_client("John", "Doe", "john@example.com", "0123456789")
        self.assertIsInstance(client, Client)
        self.assertEqual(client.full_name.first_name, "John")
        self.assertEqual(client.full_name.last_name, "Doe")
        self.assertEqual(client.email.value, "john@example.com")
        self.assertEqual(client.phone_number.value, "0123456789")
        self.mock_repository.save.assert_called_once_with(client)

    def test_register_client_email_exists_raises(self):
        existing_client = MagicMock(spec=Client)
        self.mock_repository.get_by_email.return_value = existing_client
        with self.assertRaises(ValueError) as context:
            self.service.register_client("Jane", "Smith", "john@example.com", "0123456789")
        self.assertIn("A client with this email already exists.", str(context.exception))
        self.mock_repository.save.assert_not_called()

    def test_get_client_by_id_returns_client(self):
        client_id = "123"
        expected_client = MagicMock(spec=Client)
        self.mock_repository.get_by_id.return_value = expected_client
        result = self.service.get_client_by_id(client_id)
        self.assertEqual(result, expected_client)
        self.mock_repository.get_by_id.assert_called_once_with(client_id)

    def test_get_client_by_id_returns_none(self):
        self.mock_repository.get_by_id.return_value = None
        result = self.service.get_client_by_id("non-existent-id")
        self.assertIsNone(result)

    def test_get_all_clients_returns_list(self):
        clients = [MagicMock(spec=Client), MagicMock(spec=Client)]
        self.mock_repository.get_all.return_value = clients
        result = self.service.get_all_clients()
        self.assertEqual(result, clients)
        self.mock_repository.get_all.assert_called_once()
