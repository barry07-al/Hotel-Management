import pytest

from unittest.mock import MagicMock

from src.domain.client.entities import Client
from src.domain.client.services import ClientService

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def client_service(mock_repository):
    return ClientService(mock_repository)

def test_register_client_success(mock_repository, client_service):
    mock_repository.get_by_email.return_value = None
    client = client_service.register_client("John", "Doe", "john@example.com", "0123456789")

    assert isinstance(client, Client)
    assert client.full_name.first_name == "John"
    assert client.full_name.last_name == "Doe"
    assert client.email.value == "john@example.com"
    assert client.phone_number.value == "0123456789"
    mock_repository.save.assert_called_once_with(client)

def test_register_client_email_exists_raises(mock_repository, client_service):
    existing_client = MagicMock(spec=Client)
    mock_repository.get_by_email.return_value = existing_client

    with pytest.raises(ValueError, match="A client with this email already exists."):
        client_service.register_client("Jane", "Smith", "john@example.com", "0123456789")

    mock_repository.save.assert_not_called()

def test_get_client_by_id_returns_client(mock_repository, client_service):
    client_id = "123"
    expected_client = MagicMock(spec=Client)
    mock_repository.get_by_id.return_value = expected_client

    result = client_service.get_client_by_id(client_id)
    assert result == expected_client
    mock_repository.get_by_id.assert_called_once_with(client_id)

def test_get_client_by_id_returns_none(mock_repository, client_service):
    mock_repository.get_by_id.return_value = None
    result = client_service.get_client_by_id("non-existent-id")
    assert result is None

def test_get_all_clients_returns_list(mock_repository, client_service):
    clients = [MagicMock(spec=Client), MagicMock(spec=Client)]
    mock_repository.get_all.return_value = clients

    result = client_service.get_all_clients()
    assert result == clients
    mock_repository.get_all.assert_called_once()
