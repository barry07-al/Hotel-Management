import pytest

from unittest.mock import MagicMock

from src.domain.wallet.services import WalletService
from src.application.exceptions import ApplicationError
from src.domain.wallet.value_objects import Amount, Currency
from src.domain.wallet.entities import Wallet

@pytest.fixture
def mock_wallet():
    wallet = MagicMock(spec=Wallet)
    wallet.get_balance.return_value = 100.0
    return wallet

@pytest.fixture
def mock_repo(mock_wallet):
    repo = MagicMock()
    repo.get_by_client_id.return_value = mock_wallet
    return repo

@pytest.fixture
def wallet_service(mock_repo):
    return WalletService(mock_repo)

@pytest.fixture
def client_id():
    return "client123"

def test_deposit_success(wallet_service, mock_repo, mock_wallet, client_id):
    amount = Amount(50.0, Currency.EUR)
    wallet_service.deposit(client_id, amount)
    mock_wallet.deposit.assert_called_once_with(amount)
    mock_repo.save.assert_called_once_with(mock_wallet)

def test_deposit_wallet_not_found(mock_repo, client_id):
    mock_repo.get_by_client_id.side_effect = ApplicationError(f"Wallet not found for client {client_id}.")
    wallet_service = WalletService(mock_repo)
    amount = Amount(50.0, Currency.EUR)
    with pytest.raises(ApplicationError, match=f"Wallet not found for client {client_id}."):
        wallet_service.deposit(client_id, amount)

def test_withdraw_success(wallet_service, mock_wallet, mock_repo, client_id):
    amount = 30.0
    wallet_service.withdraw(client_id, amount)
    mock_wallet.withdraw.assert_called_once_with(amount)
    mock_repo.save.assert_called_once_with(mock_wallet)

def test_withdraw_wallet_not_found(mock_repo, client_id):
    mock_repo.get_by_client_id.side_effect = ApplicationError(f"Wallet not found for client {client_id}.")
    wallet_service = WalletService(mock_repo)
    with pytest.raises(ApplicationError, match=f"Wallet not found for client {client_id}."):
        wallet_service.withdraw(client_id, 30.0)

def test_get_balance_success(wallet_service, client_id):
    balance = wallet_service.get_balance(client_id)
    assert balance == 100.0

def test_get_balance_wallet_not_found(mock_repo, client_id):
    mock_repo.get_by_client_id.side_effect = ApplicationError(f"Wallet not found for client {client_id}.")
    wallet_service = WalletService(mock_repo)
    with pytest.raises(ApplicationError, match=f"Wallet not found for client {client_id}."):
        wallet_service.get_balance(client_id)
