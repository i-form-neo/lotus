"""Module for ukrainian phone number validation"""


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
    # Удаляем все пробелы из ввода
    number = number.replace(' ', '')

    # Проверяем что начинается с +38
    if not number.startswith("+38"):
        return False

    # Проверяем длину (13 символов: +38 и 10 цифр)
    if len(number) != 13:
        return False

    # Проверяем что после +38 идут только цифры
    if not number[3:].isdigit():
        return False

    return True


def main():
    """Method for internal testing"""

    while True:
        phone = input("Enter your phone number: ").strip()
        if is_valid_ukrainian_phone(phone):
            print("✅ Phone number is valid.")
            break
        else:
            print("❌ Invalid phone number. The number must start with +38 and contain exactly 10 digits (no spaces or extra symbols). Please try again.")


if __name__ == "__main__":
    main()
