import sys

from datetime import date

from logger import logger
from domain.rooms.entities import RoomType
from domain.currency.value_objects import Currency
from application.services import HotelApplicationService


class CLI:
    def __init__(self):
        self.app = HotelApplicationService()

    def menu(self):
        logger.info("--- XYZ Hotel CLI ---")
        logger.info("1 Create Client Account")
        logger.info("2 Deposit to Wallet")
        logger.info("3 View Balance")
        logger.info("4 View Rooms Infos")
        logger.info("5 Book Room")
        logger.info("6 Confirm Booking")
        logger.info("7 Cancel Booking")
        logger.info("Any other key to exit")

    def run(self):
        while True:
            self.menu()
            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    first = input("First name: ")
                    last = input("Last name: ")
                    email = input("Email: ")
                    phone = input("Phone: ")
                    try:
                        client = self.app.create_account(first, last, email, phone)
                        logger.info(f"✅ Client created: {client.full_name.first_name} {client.full_name.last_name} (ID: {client.id})")
                    except Exception as e:
                        logger.error(f"Error creating client: {e}")
                elif choice == "2":
                    client_id = input("Client ID: ")
                    amount = float(input("Amount: "))
                    currency = Currency[input("Currency (EUR/USD/GBP/JPY/CHF): ").upper()]
                    try:
                        self.app.deposit_money(client_id, amount, currency)
                        logger.info("💸 Deposit successful.")
                    except Exception as e:
                        logger.error(f"Error depositing money: {e}")
                elif choice == "3":
                    try:
                        client_id = input("Client ID: ")

                        balance = self.app.get_balance(client_id)

                        logger.info(f"💼 Balance: {balance:.2f} EUR")
                    except Exception as e:
                        logger.error(f"Error retrieving balance: {e}")
                elif choice == "4":
                    try:
                        client_id = input("Enter your client ID: ")
                        client = self.app.get_client_by_id(client_id)
                        logger.info(f"\n--- Room Information for {client.full_name.value} ---\n")
                        for room in RoomType:
                            room.display_info()
                    except Exception as e:
                        logger.error(f"Error retrieving client: {e}")
                        continue  
                elif choice == "5":
                    try:
                        client_id = input("Client ID: ")
                        room = RoomType[input("Room type (STANDARD, SUPERIOR, SUITE): ").upper()]
                        nights = int(input("Nights: "))
                        checkin = date.fromisoformat(input("Check-in date (YYYY-MM-DD): "))
                        booking = self.app.book_room(client_id, room, nights, checkin)
                        logger.info(f"🏨 Booking created. ID: {booking.id}, Total: {booking.total_price:.2f} EUR")
                    except Exception as e:
                        logger.error(f"Error booking room : {e}")
                elif choice == "6":
                    try:
                        client_id = input("Client ID: ")
                        booking_id = input("Booking ID: ")
                        total = float(input("Total Price: "))
                        self.app.confirm_booking(client_id, booking_id, total)
                        logger.info(f"✅ Booking {booking_id} confirmed.")
                    except Exception as e:
                        logger.error(f"Error confirmation booking: {e}")
                elif choice == "7":
                    try:
                        client_id = input("Client ID: ")
                        booking_id = input("Booking ID: ")
                        self.app.cancel_booking(booking_id, client_id)
                        logger.info(f"❌ Booking {booking_id} cancelled (no refund).")
                    except Exception as e:
                        logger.error(f"Error cancelling booking : {e}")
                else:
                    logger.info("Goodbye!")
                    sys.exit()

            except Exception as e:
                logger.info(f"Error: {e}")

