# Placeholder for future Room-related Value Objects

class RoomID:
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Room ID must not be empty.")
        self.value = value

    def __str__(self):
        return self.value
