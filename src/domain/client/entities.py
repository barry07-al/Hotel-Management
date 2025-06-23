import uuid
from .value_objects import FullName, Email, PhoneNumber
from dataclasses import dataclass, field

@dataclass
class Client:

    full_name: FullName
    email: Email
    phone_number: PhoneNumber
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if not isinstance(self.full_name, FullName):
            raise TypeError("full_name must be an instance of FullName")
        if not isinstance(self.email, Email):
            raise TypeError("email must be an instance of Email")
        if not isinstance(self.phone_number, PhoneNumber):
            raise TypeError("phone_number must be an instance of PhoneNumber")
