from collections import UserDict
from typing import Dict
from datetime import datetime, timedelta

# Базовий клас для поля


class Field:
    def __init__(self, value):
        self.value = value

# Клас для поля Name


class Name(Field):
    def __str__(self):
        return self.value

# Клас для поля Phone


class Phone(Field):
    def __init__(self, phone: str, info: str):
        phone = phone.strip()
        if len(phone) == 10 and phone.isdigit():
            self.value = (phone, info)
        else:
            raise ValueError("Phone must be numeric and len == 10")

    def __str__(self):
        return f"{self.value[0]} : {self.value[1]}"

# Клас для поля словник телефонів


class Phones(UserDict):
    def __str__(self):
        return ' '.join([f"({v})" for v in self.data.values()])

# Клас для поля дата народження


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y") if self.value else "None"

# Клас для запису в книзі


class Record:
    def __init__(self, name: str):
        name = name.strip().lower()
        self.name: Name = Name(name)
        self.phones: Phones = Phones({})
        self.birthday: Birthday | None = None

    # Метод: додає телефон в словник
    def add_phone(self, phone: str, info: str):
        phone = phone.strip()
        self.phones.data[phone] = Phone(phone, info)

    # Метод: видаляє телефон з словника
    def remove_phone(self, phone: str):
        phone = phone.strip()
        del self.phones.data[phone]

    # Метод: змінює телефон в словнику
    def edit_phone(self, old_phone: str, new_phone: str, info: str):
        old_phone = old_phone.strip()
        new_phone = new_phone.strip()
        del self.phones.data[old_phone]
        self.phones.data[new_phone] = Phone(new_phone, info)

    # Метод: шукає телефон в словнику
    def find_phone(self, phone: str) -> Phone | None:
        phone = phone.strip()
        return self.phones.data.get(phone, None)

    def add_birthday(self, birthday: str):
        birthday = birthday.strip()
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {self.phones}, birthday: {self.birthday}"


# Клас для адресної книги
class AddressBook(UserDict):

    def __init__(self, dict: Dict[str, Record]):
        self.data = dict

    # Метод: додає запис в книгу
    def add_record(self, name: str, record: Record):
        name = name.strip().lower()
        self.data[name] = record

    # Метод: повертає запис з книги
    def find_record(self, name: str) -> Record | None:
        name = name.strip().lower()
        return self.data.get(name, None)

    # Метод: видаляє запис з книги
    def remove_record(self, name: str):
        name = name.strip().lower()
        del self.data[name]

    def get_upcoming_birthdays(self):
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
                        days=(7 - congratulation_date.weekday()))
                return f"{record.name}: congratulation date: {congratulation_date.strftime('%d.%m.%Y')}"
            else:
                return ""

        today = datetime.now().date()
        # Формуємо список привітань на наступні 7 днів
        return '\n'.join([make_congratulation_date(record) for record in self.data.values() if birthday_in_interval(record, 7)])

    def __str__(self):
        return '\n'.join(str(rec) for rec in self.data.values())

# Клас для поля Title

class Title(Field):
    """
    Клас Title представляє поле заголовка нотатки
    """
    def __str__(self):
        return self.value

# Клас для поля Note

class Note(Field):
    """
    Клас Note представляє поле самого тексту нотатки
    """
    def __str__(self):
        return self.value

# Клас для нотатки

class NoteRecord:
    """
    Клас NoteRecord представляє запис однієї нотатки. Поле
    id реалізовано за допомогою атрибуту класа.
    """
    _id_counter = 1

    def __init__(self, title=None, text=""):
        self.id = NoteRecord._id_counter
        NoteRecord._id_counter += 1
        self.title = Title(title if title is not None else "Без назви")
        self.text = Note(text)
        self.date_created = datetime.now()
        self.date_modified = self.date_created

    def modify(self, new_title=None, new_text=None):
        if new_title:
            self.title = Title(new_title)
        if new_text:
            self.text = Note(new_text)
        self.date_modified = datetime.now()

    def __str__(self):
        return (f"ID: {self.id}\nTitle: {self.title}\nText: {self.text}\n"
                f"Created: {self.date_created}\nModified: {self.date_modified}")

def main():
    # notes = NotesBook()

    record1 = NoteRecord(title='', text="John was a huge size")
    record1.modify(new_title="John...")
    print(record1)

    record2 = NoteRecord(title='', text="Lorem  ")
    print(record1)

    # notes.add_note(record1)

    # jane_record = Record("Jane")
    # jane_record.add_phone("9876543210")

if __name__ == "__main__":
    main()