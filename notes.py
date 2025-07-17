"""Module for notebook with notes"""

from collections import UserDict, UserList
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

# Клас для тегів


class Tags(UserList):
    """ Клас Tags - представляє список унікальних тегів"""

    def __init__(self, tag_string=""):
        initial_tags = tag_string.split(",") if tag_string else []
        unique_tags = self._normalize_and_filter(initial_tags)
        super().__init__(unique_tags)

    def _normalize_and_filter(self, tags):
        """Приймає iterable тегів та повертає унікальний список нормалізованих тегів"""
        seen = set()
        result = []
        for tag in tags:
            cleaned = tag.strip().lower()
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                result.append(cleaned)
        return result

    def add(self, tags: str):
        """Додає список тегів, уникаючи дублікатів"""
        tags = tags.split(",")
        new_tags = self._normalize_and_filter(tags)
        added = [tag for tag in new_tags if tag not in self.data]
        self.data.extend(added)

    def remove_one(self, tag: str):
        """Видаляє тег"""
        tag = tag.strip().lower()
        if tag in self.data:
            self.data.remove(tag)

    def __str__(self):
        return ", ".join(self.data)

# Клас для нотатки


class NoteRecord:
    """
    Клас NoteRecord представляє запис однієї нотатки. Поле
    id реалізовано за допомогою атрибуту класа.
    - text - обов'язковий, текст нотатки
    - title - необов'язковий, заголовок нотатки
    - tags - необов'язковий, теги нотатки, можна додати декілька "tag1, tag2, tag3"
    """

    _id_counter = 1

    def __init__(self, title=None, text="", tags=None):
        self.id = NoteRecord._id_counter
        NoteRecord._id_counter += 1
        self.title = Title(title if title is not None else "Без назви")
        self.text = Note(text)
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.tags = Tags(tags if tags else "")

    # метод редагування нотатки
    def modify(self, new_title=None, new_text=None, tags=None):
        """ метод для редагування нотатки
        - new_title - оновлений заголовок нотатки
        - new_text - оновлений текст нотатки
        - tags - теги, які додаються, можна додати декілька 
        якщо параметр не вказаний, то поле не оновлюється
        - поле date_modified в будь якому разі оновлюється на поточну дату
        """
        if new_title:
            self.title = Title(new_title)
        if new_text:
            self.text = Note(new_text)
        if tags:
            self.tags.add(tags)
        self.date_modified = datetime.now()

    def remove_tag(self, tag: str):
        """ removes tag from NoteRecord """
        if tag:
            self.tags.remove_one(tag)

    def __str__(self):
        return (f"ID: {self.id}\nTitle: {self.title}\nText: {self.text}\n"
                f"Created: {self.date_created}\nModified: {self.date_modified}\n"
                f"Tags: {self.tags.data}")

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
