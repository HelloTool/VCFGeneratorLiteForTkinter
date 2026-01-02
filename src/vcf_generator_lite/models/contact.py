import re
from typing import NamedTuple

CHINA_PHONE_PATTERN = re.compile(r"^1[356789]\d{9}$")


class Contact(NamedTuple):
    phone: str
    name: str | None = None
    note: str | None = None


class PhoneNotFoundError(ValueError):
    def __init__(self) -> None:
        super().__init__("Phone not found")


def is_china_mobile_phone(phone: str) -> bool:
    return len(phone) == 11 and CHINA_PHONE_PATTERN.match(phone) is not None


def parse_contact(contact_text: str):
    parts = contact_text.split()

    for i, part in enumerate(parts):
        if is_china_mobile_phone(part):
            phone = part
            name_parts = parts[:i]
            name = " ".join(name_parts) if name_parts else None
            note_parts = parts[i + 1 :]
            note = " ".join(note_parts) if note_parts else None
            break
    else:
        raise PhoneNotFoundError

    return Contact(
        phone=phone,
        name=name,
        note=note,
    )
