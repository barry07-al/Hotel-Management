import uuid
from .value_objects import FullName, Email, PhoneNumber
from dataclasses import dataclass, field

@dataclass
class Client:
    full_name: FullName
    email: Email
    phone_number: PhoneNumber
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
