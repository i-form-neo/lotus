import pickle
import pathlib

from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from typing import Dict, Tuple, List
from contacts import AddressBook, Record

def read_dict(path: pathlib.Path) -> Dict[str, Record]:
    """ Заванатажує довідник з файла

    path -- шлях до довідника
    """
    if path.exists():
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception as ex:
            print("Loading Contacts error: {ex}, create new dictionary")
            return {}
    else:
        # Якщо довідника ще нема, то повертаємо поржній
        return {}
    
def write_dict(path: pathlib.Path, dict: Dict[str, Record]):
    """ Записує довідник в файл

    path -- шлях до довідника
    dict -- словник довідника
    """
    with open(path, "wb") as f:
        pickle.dump(dict, f)

# Команди та їхні ариті
commands = {
    "add-phone": 2,
    "add-birthday": 2,
    "change": 3,
    "all": 0,
    "phone": 1,
    "show-birthday": 1,
    "birthdays": 0,
    "exit": 0,
    "quit": 0,
    "close": 0,
    "hello": 0,
    "help": 0
}

def main():
    script_path = pathlib.Path(__file__)
    dict_path = script_path.with_name('contacts.pickle')
    dict = read_dict(dict_path)

    console = Console()
    book = AddressBook(dict)

    # Декоратор записує словник у файл при вдалому завершенні функції
    def writer(func):
        def inner(name: str, phone: str, phone2: str | None = None) -> Tuple[bool, str]:
            res = func(name, phone, phone2)
            if res[0]:
                write_dict(dict_path, dict)
            return res
        return inner  

    # Декоратор виводить повідомлення про результат операції 
    def verbose(func):
        def inner(name: str | None = None, phone: str | None = None, phone2: str | None = None) -> Tuple[bool, str]:
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
                    if commands[res[0]] == arity:
                        for i in range(arity):
                            res[i+1] = res[i+1].strip()
                    else:
                        console.print(f"[bold red]Command '{res[0]}' expected {commands[res[0]]}, but takes {arity} parameter(s)[/bold red]")
                        res = ['error']
                else:
                    console.print(f"[bold red]Unexpected command: {' '.join(res)}[/bold red]")
                    res = ['error']
            else:
                res = ['error']

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
    def change(name: str, old_phone: str, new_phone: str) -> Tuple[bool, str]:
        record = book.find_record(name)
        if record:
            record.edit_phone(old_phone, new_phone, "")
            return True, f"Contact {name}: {old_phone} changed to {new_phone}"
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
        
    # Handler: all - виводить всі контакти
    @verbose
    def print_all(*args) -> Tuple[bool, str]:
        console.print("")
        console.print(str(book))
        return True, "[bold green]OK[/bold green]\n" 

    # Handler: phone name - виводить телефони вказаного контакту
    @verbose
    def print_phone(name: str, *args):
        record = book.find_record(name)
        if record:
            console.print(f"Phones {record.name}:  {record.phones}")   
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"
        
    # Handler: phone name - виводить вказаний контакт
    @verbose
    def show_birthday(name: str, *args):
        record = book.find_record(name)
        if record:
            console.print(f"Birthday {record.name}:  {record.birthday}")   
            return True, "OK\n"
        else:
            return False, f"[bold red]Contact {name} not found[/bold red]"
    
    # Handler: birthdays - виводить дні наролдення наступного тижня
    @verbose
    def birthdays(name: str, *args):
        report = book.get_upcoming_birthdays()
        if report:
            console.print(report)   
            return True, "[bold green]OK[/bold green]\n"
        else:
            return True, "[bold green]Empty list[/bold green]\n"
        

    history_path = script_path.with_name('.history')
    history = FileHistory(history_path) 
    completer = WordCompleter(list(commands.keys()))

    session = PromptSession(history=history, completer=completer, reserve_space_for_menu=True)

    @validate    
    def parse_input(msg_prompt: str) -> List[str]: 
        msg = session.prompt(msg_prompt)
        cmd = msg.split() 
        return cmd
    
    def print_help():
        console.print("Available commands and their arities:")
        for k, v in commands.items():
            console.print(f"    {k}/{v}")
    
    
    console.print("[bold green]Welcome to the assistant bot![/bold green]")
    console.print("Type 'help' for available commands or 'exit' | 'quit' | 'close' to quit.")
    console.print("Press [yellow]Tab[/yellow] for auto-completion.")

    while True:
        repl = parse_input("Enter a command: ")
        try:
            match repl:
                case ['add-phone', name, phone]:
                    add(name, phone)
                case ['add-birthday', name, birthday]:
                    add_birthday(name, birthday)
                case ['change', name, old_phone, new_phone]:
                    change(name, old_phone, new_phone)
                case ['all']:
                    print_all()
                case ['phone', name]:
                    print_phone(name)
                case ['show-birthday', name]:
                    show_birthday(name)
                case ['birthdays']:
                    birthdays()
                case ['exit'] | ['quit'] | ['close']:
                    console.print("[bold green]Good bye![/bold green]")
                    break
                case ['hello']:
                    console.print("[bold green]How can I help you?[/bold green]")
                case ['help']:
                    print_help()
                case ['error']:
                    console.print("")    
                case _:
                    console.print(f"[bold red]Unexpected command: {' '.join(repl)}[/bold red]")
        except Exception as ex:
            console.print(f"[bold red]{ex}[/bold red]")
    

if __name__ == "__main__":
    main()