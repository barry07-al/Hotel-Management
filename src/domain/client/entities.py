import uuid

from dataclasses import dataclass, field

from .value_objects import FullName, Email, PhoneNumber


@dataclass
class Client:
    full_name: FullName
    email: Email
    phone_number: PhoneNumber
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
