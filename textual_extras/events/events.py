from textual.events import Event


class TextChanged(Event):
    pass


class PyperclipError(Event):
    pass


class InvalidInputAttempt(Event):
    pass
