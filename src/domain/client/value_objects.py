from application.exceptions import ApplicationError

class FullName:

    def __init__(self, first_name: str, last_name: str):
        if not first_name or not last_name:
            raise ApplicationError("Both first and last names are required.")
        if " " in first_name or " " in last_name:
            raise ApplicationError("First and last names should not contain spaces.")
        self.first_name = first_name
        self.last_name = last_name
        self.value = f"{first_name} {last_name}"

class Email:
    def __init__(self, value: str):
        import re
        if not re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$", value):
            raise ApplicationError("Invalid email address.")
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.value.lower() == other.value.lower()
        return False

class PhoneNumber:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) < 10 or len(value) > 15:
            raise ApplicationError("Invalid phone number.")
        self.value = value
