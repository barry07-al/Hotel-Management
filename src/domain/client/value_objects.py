class FullName:
    def __init__(self, first_name: str, last_name: str):
        if not first_name or not last_name:
            raise ValueError("Both first and last names are required.")
        self.first_name = first_name
        self.last_name = last_name
        self.value = f"{first_name} {last_name}"

class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        self.value = value

class PhoneNumber:
    def __init__(self, value: str):
        if len(value) < 10:
            raise ValueError("Invalid phone number.")
        self.value = value
