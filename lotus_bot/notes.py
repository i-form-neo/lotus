"""Module for notebook with notes"""

from collections import UserDict, UserList
from datetime import datetime  # , timedelta
from lotus_bot.field import Field

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

    def add(self, tags):
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
    Клас NoteRecord представляє запис однієї нотатки. 
    Поле id реалізовано за допомогою атрибуту класа.
    - text - обов'язковий, текст нотатки
    - title - необов'язковий, заголовок нотатки
    - tags - необов'язковий, повинен бути рядком через кому: "tag1, tag2, tag3"
    """

    # _id_counter = 1

    def __init__(self, title=None, text="", tags=None):
        self.id = -1  # NoteRecord._id_counter
        # NoteRecord._id_counter += 1
        self.title = Title(title if title is not None else "Без назви")
        self.text = Note(text)
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.tags = Tags(tags if tags else "")

    def modify(self, new_title=None, new_text=None, tags=None):
        """ метод для редагування нотатки
        - new_title - оновлений заголовок нотатки
        - new_text - оновлений текст нотатки
        - tags - теги додаються, можна додати декілька 
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
        """ видалення тегу з об'єкту NoteRecord """
        if tag:
            self.tags.remove_one(tag)

    def __str__(self):
        return (f"ID: {self.id}\nTitle: {self.title}\nText: {self.text}\n"
                f"Created: {self.date_created}\nModified: {self.date_modified}\n"
                f"Tags: {self.tags.data}")

# Клас для індексу


class TagIndex:
    """
    Підтримка індексації по тегам. 
    модель словник де ключі - назви тегів,
    а значення список id заміток, яка містить тег
    """

    def __init__(self):
        self.index = {}

    def add_record_to_index(self, record):
        """індексує нотатку по тегу"""
        for tag in record.tags.data:
            self.index.setdefault(tag, []).append(record.id)

    def remove_record_from_index(self, note_id):
        """видаляє ID нотатки з кожного тегу в якому зустрічається"""
        for tag, ids in list(self.index.items()):
            if note_id in ids:
                ids.remove(note_id)
                if not ids:
                    del self.index[tag]

    def add_tag(self, note_id, tag):
        """ додає нотатку у індекс за тегом tag."""
        ids = self.index.setdefault(tag, [])
        if note_id not in ids:
            ids.append(note_id)

    def remove_tag(self, note_id, tag):
        """ видалення ID нотатки з списку для відповідного тега tag """
        ids = self.index.get(tag, [])
        if note_id in ids:
            ids.remove(note_id)
            if not ids:
                del self.index[tag]

    def search(self, tag):
        """повертає список id заміток з тегом"""
        return list(self.index.get(tag, []))

    def all(self):
        """повертає весь індекс."""
        return self.index

# Клас для списка нотаток


class NotesBook(UserDict):
    """
    Клас NotesBook представляє записник. 
    add_note() - додає замітку
    search_by_tags() - пошук заміток по тегам
    delete_note() - видалення замітки по id
    edit_note() - редагування замітки по id
    """

    def __init__(self, dictionary):
        super().__init__()
        self.data = dictionary
        self.tag_index = TagIndex()

    def __next_id(self) -> int:
        if len(self.data) == 0:
            return 1
        else:
            return max(self.data.keys()) + 1

    def add_note(self, record: NoteRecord):
        """
        Метод add_note() приймає один агрумент типу NoteRecord, 
        додає замітку
        """
        # self.data[record.id] = record
        id = self.__next_id()
        record.id = id
        self.data[id] = record
        self.tag_index.add_record_to_index(record)

    def search_by_tags(self, tags: str):
        """
        Повертає list of objects:NoteRecord, які мають задані теги.
        tags повинен бути рядком з тегами через кому: "tag1, tag2"
        """
        # нормалізовані вхідні теги до списку
        tag_list = [t.strip().lower() for t in tags.split(",") if t.strip()]

        # якщо не передано жодного тегу, метод повартає пустий список
        if not tag_list:
            return []

        # множини id для кожного тегу
        id_sets = []
        for tag in tag_list:
            ids = set(self.tag_index.search(tag))
            # якщо хоча б одного тегу не знайдено, метод повартає пустий список
            if not ids:
                return []
            id_sets.append(ids)

        # перетин всіх множини, щоб знайти спільні id
        common_ids = set.intersection(*id_sets)

        # список об’єктів NoteRecord за знайденими id
        return [self.data[nid] for nid in common_ids if nid in self.data]

    def delete_note(self, note_id: int):
        """
        Метод delete_note() видаляє замітку по id (int)
        """
        if note_id in self.data:
            del self.data[note_id]
            self.tag_index.remove_record_from_index(note_id)
            return True
        return False

    def edit_note(self, note_id: int, new_title=None, new_text=None, tags=None):
        """
        Метод edit_note() дозволяє редагувати замітку по id (int),
        модифікує заголовок/текст нотатки і додає нові теги в індекс.
        """
        note = self.data.get(note_id)
        if not note:
            return False

        # стан тегів ДО модифікації
        if tags:
            old_tags = set(note.tags.data)

        # беспосередньо зміни самої нотатки
        note.modify(new_title, new_text, tags)

        # порівнюємо і додаємо в індекс тільки справді нові теги
        if tags:
            new_tags = set(note.tags.data)
            added = new_tags.difference(old_tags)
            for tag in added:
                self.tag_index.add_tag(note_id, tag)
        return True

    def remove_tag(self, note_id, tag):
        """
        Видалення тегу з однієї нотатки та оновлення індексу
        """
        note = self.get(note_id)
        if not note:
            return False

        note.remove_tag(tag)
        self.tag_index.remove_tag(note_id, tag)
        return True
