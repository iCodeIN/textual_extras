from textual_extras.widgets.text_input import TextInput, View
from textual_extras.events import PyperclipError

from typing import Literal
from rich.console import RenderableType
from rich.align import AlignMethod
from rich.style import StyleType
from rich.text import Text, TextType


# Returns the  next smallest number in the table of `b` after `a`
floor = lambda a, b: b * (a // b)
# Returns the  next smallest number in the table of `b` after `a`
ceil = lambda a, b: b * ((a + b - 1) // b)


class MultiLineTextInput(TextInput):
    """
    A simple mutli-line text input widget
    """

    def __init__(
        self,
        name: str | None = None,
        title: TextType = "",
        title_align: AlignMethod = "center",
        border_style: StyleType = "blue",
        placeholder: TextType = Text("Placeholder...", style="dim white"),
        password: bool = False,
        list: tuple[Literal["blacklist", "whitelist"], list[str]] = ("blacklist", []),
        max_lines: int | None = None,
        fixed: bool = False,
    ) -> None:
        super().__init__(
            name, title, title_align, border_style, placeholder, password, list
        )
        self.max_lines = max_lines
        self.fixed = fixed

    def _set_view(self):
        """
        Sets a viewable range of text for the widget
        """

        self.max_lines = self.max_lines or (self.size.height - 2)
        self.view = View(0, self.max_lines * (self.size.width - 4))

    def _wrap_text(self, text: str) -> str:
        """
        Seperate text into chunks for proper rendering of the box
        """

        width = self.size.width - 4
        return "\n".join([text[i : i + width] for i in range(0, len(text), width)])

    def _format_text(self, text: str) -> str:
        """
        Trims out the invisible text and return the formatted text
        """

        text = text[self.view.start : self.view.end]
        return self._wrap_text(text)

    def update_view(self, prev: int, curr: int) -> None:
        """
        Updates the current view-able part of the text if there is an overflow
        """

        jump = self.size.width - 4
        if prev >= self.view.start and curr < self.view.start:
            self.view.shift_left(jump)

        elif prev <= self.view.end and curr >= self.view.end:
            self.view.shift_right(jump, max_val=ceil(len(self.value), jump))

    async def handle_keypress(self, key: str) -> None:
        """
        Handles keypresses
        """

        match key:
            # Moving backward
            case "left":
                await self._move_cursor_backward()

            case "ctrl+left":
                await self._move_cursor_backward(word=True)

            case "ctrl+h":  # Backspace (No ctrl+backspace for ya T_T)
                await self._move_cursor_backward(delete=True)

            # Moving forward
            case "right":
                await self._move_cursor_forward()

            case "ctrl+right":
                await self._move_cursor_forward(word=True)

            case "delete":
                await self._move_cursor_forward(delete=True)

            case "ctrl+delete":
                await self._move_cursor_forward(word=True, delete=True)

            # EXTRAS
            case "home":
                self._cursor_position = floor(
                    self._cursor_position, self.size.width - 4
                )

            case "ctrl+home":
                self._cursor_position = 0

            case "end":
                self._cursor_position = min(
                    ceil(self._cursor_position + 1, self.size.width - 4),
                    len(self.value),
                )

            case "ctrl+end":
                self._cursor_position = len(self.value)

            # COPY-PASTA
            case "ctrl+v":
                try:
                    await self._insert_text()
                except:
                    await self.emit(PyperclipError(self))
                    return

            case "up":
                self._cursor_position = max(
                    0, self._cursor_position - (self.size.width - 4)
                )

            case "down":
                self._cursor_position = min(
                    self._cursor_position + self.size.width - 4, len(self.value)
                )

        if len(key) == 1:
            await self._insert_text(key)

    def render_panel(self, text: TextType) -> RenderableType:
        """
        Builds a panel for the input box
        """

        if not self.fixed:
            height = 1 + ((len(self.value) - self.view.start) or 1) // (
                self.size.width - 4
            )
            # SAFETY: self.max_lines will never be `None` because...
            # it is called from within the `render` method which updates the variable, if None, to the widget height
            height = min(height, self.max_lines)
        else:
            height = self.max_lines

        return super().render_panel(text, height)
