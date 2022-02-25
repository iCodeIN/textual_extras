from .text_input import TextInput
from string import digits


class NumberInput(TextInput):
    """
    An Input Box for Numbers
    """

    def __init__(self):
        super().__init__(list=("whitelist", list(digits + " ")))
