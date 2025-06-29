import pytest

from unittest.mock import MagicMock

from src.domain.client.entities import Client


def test_register_client_success(mock_client_repository, client_service):
    mock_client_repository.get_by_email.return_value = None
    client = client_service.register_client("Alpha", "BARRY", "barry@gmail.com", "0689123546")
    assert isinstance(client, Client)
    assert client.full_name.first_name == "Alpha"
    assert client.full_name.last_name == "BARRY"
    assert client.email.value == "barry@gmail.com"
    assert client.phone_number.value == "0689123546"
    mock_client_repository.save.assert_called_once_with(client)

def test_register_client_email_exists_raises(mock_client_repository, client_service):
    existing_client = MagicMock(spec=Client)
    mock_client_repository.get_by_email.return_value = existing_client
    with pytest.raises(Exception, match="A client with this email already exists."):
        client_service.register_client("Alpha", "BARRY", "barry@gmail.com", "0689123546")
    mock_client_repository.save.assert_not_called()

def test_get_client_by_id_returns_client(mock_client_repository, client_service):
    client_id = "123"
    expected_client = MagicMock(spec=Client)
    mock_client_repository.get_by_id.return_value = expected_client
    result = client_service.get_client_by_id(client_id)
    assert result == expected_client
    mock_client_repository.get_by_id.assert_called_once_with(client_id)

def test_get_client_by_id_returns_none(mock_client_repository, client_service):
    mock_client_repository.get_by_id.return_value = None
    result = client_service.get_client_by_id("non-existent-id")
    assert result is None

def test_get_all_clients_returns_list(mock_client_repository, client_service):
    clients = [MagicMock(spec=Client), MagicMock(spec=Client)]
    mock_client_repository.get_all.return_value = clients
    result = client_service.get_all_clients()
    assert result == clients
    mock_client_repository.get_all.assert_called_once()
