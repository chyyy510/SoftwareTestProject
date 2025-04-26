class Calculator:
    """A simple calculator class."""

    def __init__(self, init_value=0):
        self.value = init_value

    def add(self, amount):
        self.value += amount
        return self.value

    def subtract(self, amount):
        self.value -= amount
        return self.value

    @classmethod
    def create_with_double(cls, value):
        return cls(value * 2)

    @staticmethod
    def multiply(a, b):
        return a * b
