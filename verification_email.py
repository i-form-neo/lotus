"""Module for email validation"""
import re


def is_valid_email(email):
    """
    Перевіряє email-адресу за допомогою регулярного виразу.

    Шаблон перевіряє:
    - Наявність літер, цифр, крапок або дефісів перед '@'
    - Доменне ім'я з літерами, цифрами або дефісами
    - Крапку та щонайменше дві літери в зоні домену верхнього рівня

    Повертає True, якщо email відповідає шаблону, інакше False.
    """
    if not email:
        return False
    pattern = r'^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def main():
    """Method for internal testing"""
    while True:
        user_email = input("Enter your email: ").strip()
        if is_valid_email(user_email):
            print("✅ Email is valid, thank you!")
            break
        else:
            print("❌ Email is not valid. Try again")


if __name__ == "__main__":
    main()
