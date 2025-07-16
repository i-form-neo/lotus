def is_valid_ukrainian_phone(number):
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
    while True:
        phone = input("Enter your phone number: ").strip()
        if is_valid_ukrainian_phone(phone):
            print("✅ Phone number is valid.")
            break
        else:
            print("❌ Invalid phone number. The number must start with +38 and contain exactly 10 digits (no spaces or extra symbols). Please try again.")

if __name__ == "__main__":
    main()