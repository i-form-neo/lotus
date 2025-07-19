"""Main module for assistant bot"""
from __future__ import annotations

import pathlib
import pickle
import shlex
import sys
from typing import Dict
from typing import List
from typing import Tuple

from appdirs import user_data_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console

from lotus_bot.contacts import AddressBook
from lotus_bot.contacts import Record
from lotus_bot.notes import NoteRecord
from lotus_bot.notes import NotesBook
from lotus_bot.rich_table_printer import print_as_rich_table


app_name = "Lotus"
app_author = "i-form"


def read_dict(path: pathlib.Path) -> Dict:
    """Заванатажує довідник з файла

    path -- шлях до довідника
    """
    if path.exists():
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print(f"Loading Contacts error: {ex}, create new dictionary")
            return {}
    else:
        # Якщо довідника ще нема, то повертаємо поржній
        return {}


def write_dict(path: pathlib.Path, dictionary: Dict):
    """Записує довідник в файл

    path -- шлях до довідника
    dict -- словник довідника
    """
    with open(path, "wb") as f:
        pickle.dump(dictionary, f)


# Команди та їхні ариті
commands = {
    "add-phone": 2,
    "add-birthday": 2,
    "add-email": 2,
    "add-address": 2,
    "change": 3,
    "remove": 1,
    "all": 0,
    "phone": 1,
    "show-birthday": 1,
    "birthdays": 1,
    "find-by-phone": 1,
    "find-by-email": 1,
    "add-note": 2,
    "edit-note": 3,
    "remove-note": 1,
    "all-notes": 0,
    "exit": 0,
    "quit": 0,
    "close": 0,
    "hello": 0,
    "help": 0,
}

# Команди та їхнє використання
command_usage = {
    "add-phone": 'Add new contact or phone: name phone (add-phone "John Dou" +380123334455)',
    "add-birthday": 'Add or update birthday: name birthday (add-birthday "John Dou" 22.07.2000)',
    "add-email": 'Add or update email: name email (add-email "John Dou" john.dou@example.com)',
    "add-address": 'Add or update address: name address (add-address "John Dou" "Kyiv, Ukraine")',
    "change": 'Update phone: name old-phone new-phone (change "John Dou" +380123334455 +380245556677)',
    "remove": 'Remove contact: name (remove "John Dou")',
    "all": "Print all contacts: all [sort-by-column, desc|reverse|true] (all birthday desc)",
    "phone": 'Print phones: name (phone "John Dou")',
    "show-birthday": 'Print birthday: name (show-birthday "John Dou")',
    "birthdays": "Print birthdays next n day: n_day (birthdays 10)",
    "find-by-phone": "Find and print contact by phone: phone (find-by-phone +380123334455)",
    "find-by-email": "Find and print contact by email: email (find-by-email john.dou@example.com)",
    "add-note": 'Add new note: title text (add-note "New note" "text to be noted")',
    "edit-note": 'Update note: id title text (edit-note 1 "Edited title" "Edited text to be noted")',
    "remove-note": "Remove note: id (remove-note 1)",
    "all-notes": "Print all notes: all-notes [sort-by-column, desc|reverse|true] (all-notes created desc)",
    "exit": "Close bot",
    "quit": "Close bot",
    "close": "Close bot",
    "hello": "Hello bot",
    "help": "Print this usage",
}


def main():
    """Entry point for Assistant Bot"""

    console = Console()

    data_path = pathlib.Path(user_data_dir(app_name, app_author))
    if not data_path.exists():
        data_path.mkdir(parents=True, exist_ok=True)
    elif not data_path.is_dir():
        console.print(f"[bold red]Path {data_path} is not dir![/bold red]")
        sys.exit(1)

    dict_path = data_path.joinpath("lotus.pickle")
    dictionary = read_dict(dict_path)

    if len(dictionary) == 0:
        book = AddressBook({})
        dictionary["contacts"] = book.data
        notes_book = NotesBook({})
        dictionary["notes"] = notes_book.data
    else:
        book = AddressBook(dictionary["contacts"])
        notes_book = NotesBook(dictionary["notes"])

    # Декоратор записує словник у файл при вдалому завершенні функції

    def writer(func):
        def inner(name: str, *args) -> Tuple[bool, str]:

            res = func(name, *args)
            if res[0]:
                write_dict(dict_path, dictionary)
            return res

        return inner

    # Декоратор виводить повідомлення про результат операції
    def verbose(func):
        def inner(
            name: str | None = None, phone: str | None = None, phone2: str | None = None
        ) -> Tuple[bool, str]:
            res = func(name, phone, phone2)
            console.print(res[1])
            return res

        return inner

    # Декоратор приводить команди до нижнього регістру
    # та паервіряє ариті команди (кількість параметрів)
    def validate(func):
        def inner(msg_prompt: str) -> List[str]:
            res: List[str] = func(msg_prompt)
            if len(res) > 0:
                res[0] = res[0].strip().lower()
                arity = len(res) - 1
                if res[0] in commands:
                    if commands[res[0]] <= arity:
                        for i in range(arity):
                            res[i + 1] = res[i + 1].strip()
                    else:
                        console.print(
                            f"[bold red]Command '{res[0]}' expected {commands[res[0]]}, but takes {arity} parameter(s)[/bold red]"
                        )
                        res = ["error"]
                else:
                    console.print(
                        f"[bold red]Unexpected command: {' '.join(res)}[/bold red]"
                    )
                    res = ["error"]
            else:
                res = ["error"]

            return res

        return inner

    # Handler: add name phone - додає новий контакт
    @writer
    @verbose
    def add(name: str, phone: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.add_phone(phone, "")
        else:
            record = Record(name)
            record.add_phone(phone, "")
            book.add_record(name, record)
        return True, f"Phone {phone} to {name} added"

    # Handler: change name phone - змінює існуючий контакт
    @writer
    @verbose
    def change(name: str, old_phone: str, new_phone: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.edit_phone(old_phone, new_phone, "")
            return True, f"Contact {name}: {old_phone} changed to {new_phone}"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"

    # Handler: remove name  - видаляє існуючий контакт
    @writer
    @verbose
    def remove(name: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            book.remove_record(name)
            return True, f"Contact {name} removed"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"

    # Handler: add-birthday name dd.mm.yyyy
    @writer
    @verbose
    def add_birthday(name: str, birthday: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.add_birthday(birthday)
        else:
            record = Record(name)
            record.add_birthday(birthday)
            book.add_record(name, record)
        return True, f"Birthday {birthday} to {name} added"

    # Handler: add-email name email
    @writer
    @verbose
    def add_email(name: str, email: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.add_email(email)
        else:
            record = Record(name)
            record.add_email(email)
            book.add_record(name, record)
        return True, f"Email {email} to {name} added"

    # Handler: add-address name address
    @writer
    @verbose
    def add_address(name: str, address: str, *args) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.add_address(address)
        else:
            record = Record(name)
            record.add_address(address)
            book.add_record(name, record)
        return True, f"Address {address} to {name} added"

    def print_all(*args) -> Tuple[bool, str]:
        sort_by, reverse_sort = sort_params(args)

        print_as_rich_table(
            columns=[
                {"name": "Name", "min_width": 20, "max_width": 30, "no_wrap": False},
                {"name": "Birthday", "min_width": 10},
                {
                    "name": "Address",
                    "justify": "right",
                    "no_wrap": False,
                    "max_width": 30,
                },
                {
                    "name": "Phones",
                    "justify": "right",
                    "no_wrap": False,
                    "max_width": 16,
                },
                {"name": "Email", "justify": "right"},
            ],
            rows=[
                [
                    record.name,
                    record.birthday.value if record.birthday else "",
                    record.address,
                    record.phones,
                    record.email,
                ]
                for record in book.values()
            ],
            sort_by=sort_by,
            reverse_sort=reverse_sort,
        )
        return True, "[bold green]OK[/bold green]\n"

    def sort_params(args):
        sort_by = ""
        reverse_sort = False
        if args:
            sort_by = args[0]
            if len(args) > 1:
                reverse_sort = args[1].lower() in {"desc", "reverse", "true"}
        return sort_by, reverse_sort

    # Handler: phone name - виводить телефони вказаного контакту
    @verbose
    def print_phone(name: str, *args):
        record = book.find_record(name)
        if record:
            console.print(f"Phones {record.name}:  {record.phones}")
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"

    # Handler: birthdays - виводить день народження за іменем
    @verbose
    def show_birthday(name: str, *args):
        record = book.find_record(name)
        if record:
            console.print(f"Birthday {record.name}:  {record.birthday}")
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"

    # Handler: birthdays - виводить дні народження наступного тижня
    @verbose
    def birthdays(*args):
        n_day = int(args[0])
        report = book.get_upcoming_birthdays(n_day)
        if report:
            console.print(report)
            return True, "[bold green]OK[/bold green]\n"
        else:
            return True, "[bold green]Empty list[/bold green]\n"

    # Handler: find-by-phone - шукає та виводить контакт за телефоном
    @verbose
    def find_by_phone(phone: str, *args):
        record = book.find_record_by_phone(phone)
        if record:
            console.print(record)
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact with phone {phone} not found[/bold red]"

    # Handler: find-by-email - шукає та виводить контакт за email
    @verbose
    def find_by_email(email: str, *args):
        record = book.find_record_by_email(email)
        if record:
            console.print(record)
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact with email {email} not found[/bold red]"

    # Handler: add-note title text - додає нову нотатку

    @writer
    @verbose
    def add_note(title: str, *args) -> Tuple[bool, str]:
        record = NoteRecord(title, args[0])
        notes_book.add_note(record)
        return True, f"Note '{title}' added"

    # Handler: edit-note id title text - додає нову нотатку

    @writer
    @verbose
    def edit_note(id: str, title: str, text: str, *args) -> Tuple[bool, str]:
        notes_book.edit_note(int(id), title, text)
        return True, f"Note '{title}' updated"

    # Handler: edit-note id title text - додає нову нотатку

    @writer
    @verbose
    def remove_note(id: str, *args) -> Tuple[bool, str]:
        notes_book.delete_note(int(id))
        return True, f"Note '{title}' removed"

    # Handler: all-notes виводить всі нотатки у вигляді таблиці
    def all_notes(*args) -> Tuple[bool, str]:
        sort_by, reverse_sort = sort_params(args)

        print_as_rich_table(
            columns=[
                {"name": "Id", "min_width": 2, "max_width": 6},
                {"name": "Title", "min_width": 10, "max_width": 20},
                {"name": "Text", "justify": "left", "no_wrap": False, "min_width": 30},
                {
                    "name": "Created",
                    "justify": "right",
                    "no_wrap": False,
                    "max_width": 12,
                },
                {
                    "name": "Modified",
                    "justify": "right",
                    "no_wrap": False,
                    "max_width": 12,
                },
            ],
            rows=[
                [
                    id,
                    record.title,
                    record.text,
                    record.date_created,
                    record.date_modified,
                ]
                for id, record in notes_book.items()
            ],
            sort_by=sort_by,
            reverse_sort=reverse_sort,
        )
        return True, "[bold green]OK[/bold green]\n"

    history_path = data_path.joinpath(".history")
    history = FileHistory(history_path)
    completer = WordCompleter(list(commands.keys()))

    session = PromptSession(
        history=history, completer=completer, reserve_space_for_menu=True
    )

    @validate
    def parse_input(msg_prompt: str, *args) -> List[str]:
        msg = session.prompt(msg_prompt)

        # cmd = msg.split()
        cmd = shlex.split(msg)
        return cmd

    def print_help():
        console.print("Available commands and their arities:")
        for k, v in commands.items():
            console.print(f"    {k}/{v} -- {command_usage.get(k, '')}")

    console.print("[bold green]Welcome to the assistant bot![/bold green]")
    print_help()
    console.print("Press [yellow]Tab[/yellow] for auto-completion.")

    while True:
        try:
            repl = parse_input("Enter a command: ")
            match repl:
                case ["add-phone", name, phone]:
                    add(name, phone)
                case ["add-birthday", name, birthday]:
                    add_birthday(name, birthday)
                case ["add-email", name, email]:
                    add_email(name, email)
                case ["add-address", name, address]:
                    add_address(name, address)
                case ["change", name, old_phone, new_phone]:
                    change(name, old_phone, new_phone)
                case ["remove", name]:
                    remove(name)
                case ["all", *args]:
                    print_all(*args)
                case ["phone", name]:
                    print_phone(name)
                case ["show-birthday", name]:
                    show_birthday(name)
                case ["birthdays", n_day]:
                    birthdays(n_day)
                case ["find-by-phone", phone]:
                    find_by_phone(phone)
                case ["find-by-email", email]:
                    find_by_email(email)
                case ["add-note", title, *args]:
                    add_note(title, *args)
                case ["edit-note", id, title, text, *args]:
                    edit_note(id, title, text, *args)
                case ["remove-note", id]:
                    remove_note(id)
                case ["all-notes", *args]:
                    all_notes(*args)
                case ["exit"] | ["quit"] | ["close"]:
                    console.print("[bold green]Good bye![/bold green]")
                    break
                case ["hello"]:
                    console.print("[bold green]How can I help you?[/bold green]")
                case ["help"]:
                    print_help()
                case ["error"]:
                    console.print("")
                case _:
                    console.print(
                        f"[bold red]Unexpected command: {' '.join(repl)}[/bold red]"
                    )
        except Exception as ex:
            console.print(f"[bold red]{ex}[/bold red]")


if __name__ == "__main__":
    main()
