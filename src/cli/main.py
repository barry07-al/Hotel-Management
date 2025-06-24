from application.services import HotelApplicationService
from domain.rooms.entities import RoomType
from domain.currency.value_objects import Currency
from datetime import date
import sys

app = HotelApplicationService()

def menu():
    print("\n--- Hotel CLI ---")
    print("1. Create Client Account")
    print("2. Deposit to Wallet")
    print("3. View Balance")
    print("4. Book Room")
    print("5. Confirm Booking")
    print("6. Cancel Booking")
    print("7. List Clients")
    print("8. Exit")

def cli():
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                first = input("First name: ")
                last = input("Last name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                client = app.create_account(first, last, email, phone)
                print(f"✅ Client created: {client.full_name.first_name} {client.full_name.last_name} (ID: {client.id})")

            elif choice == "2":
                user_id = input("Client ID: ")
                amount = float(input("Amount: "))
                currency = Currency[input("Currency (EUR/USD/GBP/JPY/CHF): ").upper()]
                app.deposit_money(user_id, amount, currency)
                print("💸 Deposit successful.")

            elif choice == "3":
                user_id = input("Client ID: ")
                balance = app.get_balance(user_id)
                print(f"💼 Balance: {balance:.2f} EUR")

            elif choice == "4":
                user_id = input("Client ID: ")
                room = RoomType[input("Room type (STANDARD, SUPERIOR, SUITE): ").upper()]
                nights = int(input("Nights: "))
                checkin = date.fromisoformat(input("Check-in date (YYYY-MM-DD): "))
                booking = app.book_room(user_id, room, nights, checkin)
                print(f"🏨 Booking created. ID: {booking.id}, Total: {booking.total_price:.2f} EUR")

            elif choice == "5":
                user_id = input("Client ID: ")
                booking_id = input("Booking ID: ")
                total = float(input("Total Price: "))
                app.confirm_booking(user_id, booking_id, total)
                print("✅ Booking confirmed.")

            elif choice == "6":
                user_id = input("Client ID: ")
                booking_id = input("Booking ID: ")
                app.cancel_booking(booking_id, user_id)
                print("❌ Booking cancelled (no refund).")

            elif choice == "7":
                for c in app.list_clients():
                    print(f"🧑 {c.full_name.first_name} {c.full_name.last_name} - {c.email.value}")

            elif choice == "8":
                print("Goodbye!")
                sys.exit()

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")
