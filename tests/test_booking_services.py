import pytest

from datetime import date
from unittest.mock import MagicMock, patch

from src.domain.rooms.entities import RoomType
from src.application.services import BookingService


@pytest.fixture(autouse=True)
def mock_persistence():
    with patch("src.application.services.Persistence.load_reservations", return_value=[]), \
         patch("src.application.services.Persistence.save_reservations"):
        yield

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def booking_service(mock_repo):
    return BookingService(repo=mock_repo)

@pytest.fixture
def client_id():
    return "client-123"

@pytest.fixture
def booking_id():
    return "booking-123"

def test_create_booking(booking_service, mock_repo, client_id):
    nights = 2
    checkin = date(2025, 6, 25)
    room_type = RoomType.STANDARD
    booking = booking_service.create_booking(client_id, room_type, nights, checkin)
    assert booking.client_id == client_id
    assert booking.room_type == room_type
    mock_repo.save.assert_called_once_with(booking)

def test_confirm_booking_success(booking_service, mock_repo, booking_id):
    mock_reservation = MagicMock()
    mock_repo.get_by_id.return_value = mock_reservation

    booking_service.confirm_booking(booking_id)

    mock_reservation.confirm.assert_called_once()
    mock_repo.get_by_id.assert_called_once_with(booking_id)

def test_cancel_booking_success(booking_service, mock_repo, booking_id, client_id):
    mock_reservation = MagicMock()
    mock_repo.get_by_id.return_value = mock_reservation

    booking_service.cancel_booking(booking_id, client_id)

    mock_reservation.cancel.assert_called_once_with(client_id)
    mock_repo.get_by_id.assert_called_once_with(booking_id)

def test_cancel_booking_not_found(booking_service, mock_repo, booking_id, client_id):
    mock_repo.get_by_id.return_value = None


    with pytest.raises(ValueError, match=f"Booking {booking_id} not found."):
        booking_service.cancel_booking(booking_id, client_id)

    mock_repo.get_by_id.assert_called_once_with(booking_id)
