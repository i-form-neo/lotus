# Базовий клас для поля

class Field:
    """Base class for field"""

    def __init__(self, value):
        print(f"Field inited with {value}")
        self.value = value
