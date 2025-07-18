"""Module for address book with phones and birthdays for contacts"""

from collections import UserDict
from typing import Dict
from datetime import datetime, timedelta

from field import Field
from verification_phone_number import is_valid_ukrainian_phone
from verification_email import is_valid_email


class Name(Field):
    """Class for name field"""

    def __str__(self):
        return self.value


class Phone(Field):
    """Class for Phone field"""

    def __init__(self, phone: str, info: str):
        phone = phone.strip()
        if not is_valid_ukrainian_phone(phone):
            raise ValueError(
                "❌ Invalid phone number. It must start with +38 and contain exactly 10 digits."
            )
        super().__init__((phone, info))

    def __str__(self):
        return f"{self.value[0]}{':' + self.value[1] if self.value[1] else ''} "


class Phones(UserDict):
    """Class for Phone field"""

    def __str__(self):
        return ' '.join([f"{v}" for v in self.data.values()])


class Birthday(Field):
    """Class for Birthday field"""

    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y") if self.value else "None"


class Email(Field):
    """Class for email field"""

    def __init__(self, email: str):
        email = email.strip()
        if not is_valid_email(email):
            raise ValueError("Invalid email address format")
        super().__init__(email)

    def __str__(self):
        return f"{self.value}"


class Address(Field):
    """Class for address field"""

    def __init__(self, address: str):
        address = address.strip()
        super().__init__(address)

    def __str__(self):
        return f"{self.value}"


class Record:
    """Class for an Address Book record"""

    def __init__(self, name: str):
        name = name.strip()
        self.name: Name = Name(name)
        self.phones: Phones = Phones({})
        self.birthday: Birthday | None = None
        self.email: Email | None = None
        self.address: Address | None = None

    def add_phone(self, phone: str, info: str):
        """Adds phone and additional info to the Record"""

        phone = phone.strip()
        self.phones.data[phone] = Phone(phone, info)

    def remove_phone(self, phone: str):
        """Removes phone from the Record"""

        phone = phone.strip()
        del self.phones.data[phone]

    def edit_phone(self, old_phone: str, new_phone: str, info: str):
        """Changes phone in the Record from old_phone to new_phone"""

        old_phone = old_phone.strip()
        new_phone = new_phone.strip()
        del self.phones.data[old_phone]
        self.phones.data[new_phone] = Phone(new_phone, info)

    def find_phone(self, phone: str) -> Phone | None:
        """Finds phone in the Record and returns it, if not found returns None"""

        phone = phone.strip()
        return self.phones.data.get(phone, None)

    def add_birthday(self, birthday: str):
        """Adds birthday to the Record"""

        birthday = birthday.strip()
        self.birthday = Birthday(birthday)

    def add_email(self, email: str):
        email = email.strip()
        self.email = Email(email)

    def add_address(self, address: str):
        address = address.strip()
        self.address = Address(address)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {self.phones}, birthday: {self.birthday}, email: {self.email}, address: {self.address}"


class AddressBook(UserDict):
    """Class representing Address Book"""

    def __init__(self, dictionary: Dict[str, Record]):
        self.data = dictionary

    def add_record(self, name: str, record: Record):
        """Adds new Record to the Address Book"""

        name = name.strip().lower()
        self.data[name] = record

    def find_record(self, name: str) -> Record | None:
        """Finds and returns Record in the Address Book by name"""

        name = name.strip().lower()
        return self.data.get(name, None)
    
    def find_record_by_phone(self, phone: str) -> Record | None:
        """Finds and returns Record in the Address Book by phone"""

        for (k, v) in self.data.items():
            if phone in v.phones:
                return self.data.get(k, None)
        return None
    
    def find_record_by_email(self, email: str) -> Record | None:
        """Finds and returns Record in the Address Book by email"""

        for (k, v) in self.data.items():
            if v.email is not None and email == v.email.value:
                return self.data.get(k, None)
        return None

    def remove_record(self, name: str):
        """Removes Record from the Address Book by name"""

        name = name.strip().lower()
        del self.data[name]

    def get_upcoming_birthdays(self, n_day: int = 7):
        """Returns string representing list of Records whome to congratulate in next 7 days"""
        # Функція перевіряє чи дата потрапляє в потрібний інтервал дат
        def birthday_in_interval(record: Record, n_day) -> bool:
            if record.birthday:
                today = datetime.today()
                year = today.year
                month = record.birthday.value.month
                day = record.birthday.value.day

                birthday = datetime(year, month, day)
                delta = (birthday - today).days
                if delta < n_day and delta >= 0:
                    return True
                birthday = datetime(year + 1, month, day)
                delta = (birthday - today).days
                if delta < n_day and delta >= 0:
                    return True
                return False

            else:
                return False

        # Функція створює рядок привітання (при потребі зсуває дату на понеділок)
        def make_congratulation_date(record: Record):

            if record.birthday:
                today = datetime.today()
                year = today.year
                month = record.birthday.value.month
                day = record.birthday.value.day

                congratulation_date = datetime(year, month, day)
                if congratulation_date < today:
                    congratulation_date = datetime(year + 1, month, day)

                if congratulation_date.weekday() > 4:
                    congratulation_date += timedelta(
                        days=7 - congratulation_date.weekday())
                return f"{record.name}: congratulation date: {congratulation_date.strftime('%d.%m.%Y')}"
            else:
                return ""

        # Формуємо список привітань на наступні n_day днів
        return '\n'.join([make_congratulation_date(record) for record in self.data.values() if birthday_in_interval(record, n_day)])

    def __str__(self):
        return '\n'.join(str(rec) for rec in self.data.values())
