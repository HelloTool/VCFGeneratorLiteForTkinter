import re
from typing import NamedTuple

CHINA_PHONE_PATTERN = re.compile(r"^1[356789]\d{9}$")


class Contact(NamedTuple):
    name: str
    phone: str


def is_china_phone(phone: str) -> bool:
    return CHINA_PHONE_PATTERN.match(phone) is not None


def parse_contact(person_text: str):
    info_list: list[str] = person_text.rsplit(None, 1)
    if len(info_list) != 2:
        raise ValueError(f"The person info is illegal: '{person_text}'.")
    name, phone = info_list
    if not name:
        raise ValueError(f"The name is illegal: '{name}'.")
    if not is_china_phone(phone):
        raise ValueError(f"The phone number is illegal: '{phone}'.")
    return Contact(name, phone)
