import unittest
from unittest.mock import MagicMock
from src.domain.wallet.value_objects import Amount
from src.domain.wallet.entities import Wallet
from src.domain.wallet.services import WalletService
from src.domain.wallet.value_objects import Currency

class TestWalletService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.wallet_service = WalletService(self.mock_repo)
        self.client_id = "client123"
        self.mock_wallet = MagicMock(spec=Wallet)
        self.mock_wallet.get_balance.return_value = 100.0
        self.mock_repo.get_by_client_id.return_value = self.mock_wallet

    def test_deposit_success(self):
        amount = Amount(50.0, Currency.EUR)
        self.wallet_service.deposit(self.client_id, amount)
        self.mock_wallet.deposit.assert_called_once_with(amount)
        self.mock_repo.save.assert_called_once_with(self.mock_wallet)

    def test_deposit_wallet_not_found(self):
        self.mock_repo.get_by_client_id.return_value = None
        amount = Amount(50.0, Currency.EUR)
        with self.assertRaises(ValueError) as cm:
            self.wallet_service.deposit(self.client_id, amount)
        self.assertEqual(str(cm.exception), "Wallet not found.")

    def test_withdraw_success(self):
        amount = 30.0
        self.wallet_service.withdraw(self.client_id, amount)
        self.mock_wallet.withdraw.assert_called_once_with(amount)
        self.mock_repo.save.assert_called_once_with(self.mock_wallet)

    def test_withdraw_wallet_not_found(self):
        self.mock_repo.get_by_client_id.return_value = None
        with self.assertRaises(ValueError) as cm:
            self.wallet_service.withdraw(self.client_id, 30.0)
        self.assertEqual(str(cm.exception), "Wallet not found.")

    def test_get_balance_success(self):
        balance = self.wallet_service.get_balance(self.client_id)
        self.assertEqual(balance, 100.0)
        self.mock_repo.get_by_client_id.assert_called_once_with(self.client_id)

    def test_get_balance_wallet_not_found(self):
        self.mock_repo.get_by_client_id.return_value = None
        with self.assertRaises(ValueError) as cm:
            self.wallet_service.get_balance(self.client_id)
        self.assertEqual(str(cm.exception), "Wallet not found.")
