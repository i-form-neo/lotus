"""Module for address book with phones and birthdays for contacts"""

from collections import UserDict
from typing import Dict
from datetime import datetime, timedelta

def is_valid_ukrainian_phone(number):
    """
    Перевіряє номер телефону України у форматі +38XXXXXXXXXX.

    Логіка:
    - Видаляє всі пробіли з введеного рядка.
    - Перевіряє, чи починається номер з '+38'.
    - Перевіряє, що загальна довжина дорівнює 13 символів (+38 і 10 цифр).
    - Перевіряє, що після '+38' всі символи є цифрами.

    Повертає True, якщо номер валідний, інакше False.
    """
    number = number.replace(' ', '')

    if not number.startswith("+38"):
        return False

    if len(number) != 13:
        return False

    if not number[3:].isdigit():
        return False

    return True
  
class Field:
    """Base class for field"""
  
    def __init__(self, value):
        print(f"Field inited with {value}")
        self.value = value


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
        super().__init__((phone,info))
        
    def __str__(self):
        return f"{self.value[0]} : {self.value[1]}"


class Phones(UserDict):
    """Class for Phone field"""

    def __str__(self):
        return ' '.join([f"({v})" for v in self.data.values()])


class Birthday(Field):
    """Class for Birthday field"""

    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y") if self.value else "None"


class Record:
    """Class for an Address Book record"""

    def __init__(self, name: str):
        name = name.strip().lower()
        self.name: Name = Name(name)
        self.phones: Phones = Phones({})
        self.birthday: Birthday | None = None

    # Метод: додає телефон в словник
    def add_phone(self, phone: str, info: str):
        """Adds phone and additional info to the Record"""

        phone = phone.strip()
        self.phones.data[phone] = Phone(phone, info)

    # Метод: видаляє телефон з словника
    def remove_phone(self, phone: str):
        """Removes phone from the Record"""

        phone = phone.strip()
        del self.phones.data[phone]

    # Метод: змінює телефон в словнику
    def edit_phone(self, old_phone: str, new_phone: str, info: str):
        """Changes phone in the Record from old_phone to new_phone"""

        old_phone = old_phone.strip()
        new_phone = new_phone.strip()
        del self.phones.data[old_phone]
        self.phones.data[new_phone] = Phone(new_phone, info)

    # Метод: шукає телефон в словнику
    def find_phone(self, phone: str) -> Phone | None:
        """Finds phone in the Record and returns it, if not found returns None"""

        phone = phone.strip()
        return self.phones.data.get(phone, None)

    def add_birthday(self, birthday: str):
        """Adds birthday to the Record"""

        birthday = birthday.strip()
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {self.phones}, birthday: {self.birthday}"


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

    # Метод: видаляє запис з книги
    def remove_record(self, name: str):
        """Removes Record from the Address Book by name"""

        name = name.strip().lower()
        del self.data[name]

    def get_upcoming_birthdays(self):
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

        # Формуємо список привітань на наступні 7 днів
        return '\n'.join([make_congratulation_date(record) for record in self.data.values() if birthday_in_interval(record, 7)])

    def __str__(self):
        return '\n'.join(str(rec) for rec in self.data.values())
