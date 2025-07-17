"""Module for notebook with notes"""

from collections import UserDict
from datetime import datetime#, timedelta
from field import Field

# Клас для поля Title


class Title(Field):
    """Клас Title представляє поле заголовка нотатки"""

    def __str__(self):
        return self.value

# Клас для поля Note


class Note(Field):
    """Клас Note представляє поле самого тексту нотатки"""

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

# Клас для списка нотаток


class NotesBook(UserDict):
    """
    Клас NotesBook представляє увесь записник. За допомогою методів класу add_note(), get_note(), edit_note(), delete_note()
        реалізовано управління нотатником.
    """

    def add_note(self, record: NoteRecord):
        """
        Метод add_note() приймає один агрумент типу NoteRecord
        """
        self.data[record.id] = record

    def get_note(self, note_id):
        """
        Методи get_note() приймає один аргумент порядковий номер нотатки
        """
        return self.data.get(note_id)

    def delete_note(self, note_id):
        """
        Методи delete_note() приймає один аргумент порядковий номер нотатки
        """
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False

    def edit_note(self, note_id, new_title=None, new_text=None):
        """
        Метод edit_note() приймає один обов'язковий параметр id, та два ключових необов'язкових параметри
        new_title, new_text, вказане поле залишається без змін, якщо нічого не передано
        """
        note = self.get_note(note_id)
        if note:
            note.modify(new_title, new_text)
            return True
        return False
