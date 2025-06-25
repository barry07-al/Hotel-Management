
import unittest

from datetime import date
from unittest.mock import MagicMock, patch

from src.domain.rooms.entities import RoomType
from src.application.services import BookingService

class TestBookingService(unittest.TestCase):

    def setUp(self):
        self.client_id_test = "client-123"
        self.booking_id_test = "booking-123"

        self.mock_repo = MagicMock()
        patcher = patch('src.application.services.Persistence.load_reservations', return_value=[])
        self.addCleanup(patcher.stop)
        patcher.start()
        patch('src.application.services.Persistence.save_reservations').start()
        self.service = BookingService(repo=self.mock_repo)

    def tearDown(self):
        patch.stopall()

    def test_create_booking(self):
        nights = 2
        checkin = date(2025, 6, 25)
        room_type = RoomType.STANDARD
        booking = self.service.create_booking(self.client_id_test, room_type, nights, checkin)
        self.assertEqual(booking.client_id, self.client_id_test)
        self.assertEqual(booking.room_type, room_type)
        self.mock_repo.save.assert_called_once_with(booking)

    def test_confirm_booking_success(self):
        mock_reservation = MagicMock()
        self.mock_repo.get_by_id.return_value = mock_reservation
        self.service.confirm_booking(self.booking_id_test)
        mock_reservation.confirm.assert_called_once()
        self.mock_repo.get_by_id.assert_called_with(self.booking_id_test)

    def test_cancel_booking_success(self):
        mock_reservation = MagicMock()
        self.mock_repo.get_by_id.return_value = mock_reservation
        self.service.cancel_booking(self.booking_id_test, self.client_id_test)
        mock_reservation.cancel.assert_called_once_with(self.client_id_test)
        self.mock_repo.get_by_id.assert_called_with(self.booking_id_test)

    def test_cancel_booking_not_found(self):
        self.mock_repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.service.cancel_booking(self.booking_id_test, self.client_id_test)
        self.assertEqual(str(context.exception), "Reservation not found.")
        self.mock_repo.get_by_id.assert_called_with(self.booking_id_test)
