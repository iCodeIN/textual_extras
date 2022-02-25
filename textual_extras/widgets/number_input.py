from .text_input import TextInput
from string import digits


class NumberInput(TextInput):
    def __init__(self):
        super().__init__(list=("whitelist", list(digits + " ")))
