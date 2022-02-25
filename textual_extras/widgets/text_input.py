from typing import Literal
from rich.box import SQUARE
from rich.align import AlignMethod
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType

from textual import events
from textual.reactive import Reactive
from textual.widget import Widget
from rich.console import RenderableType

import pyperclip

from ..events import TextChanged, PyperclipError, InvalidInputAttempt


class View:
    def __init__(self, start: int = 0, end: int = 0) -> None:
        self.start = start
        self.end = end

    def __str__(self):
        return f"View({self.start}, {self.end})"


class TextInput(Widget):
    """
    A simple single line Text Input widget
    """

    value: str = ""
    cursor: str = "|"
    _cursor_position: int = 0
    _has_focus: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        *,
        name: str | None = None,
        title: TextType = "",
        title_align: AlignMethod = "center",
        border_style: StyleType = "blue",
        placeholder: TextType = Text("Placeholder ...", style="dim white"),
        password: bool = False,
        list: tuple[Literal["blacklist", "whitelist"], list[str]] = ("blacklist", []),
    ) -> None:
        super().__init__(name)
        self.title = title
        self.title_align: AlignMethod = title_align  # Silence compiler warning
        self.border_style: StyleType = border_style
        self.placeholder = placeholder
        self.password = password
        self.list = list

        self._cursor_position = len(self.value)

    @property
    def has_focus(self) -> bool:
        return self._has_focus

    def render(self) -> RenderableType:
        """
        Renders a Panel for the Text Input Box
        """

        if not hasattr(self, "view"):
            self.view = View(0, self.size.width - 4)

        if self.has_focus:
            text = self._render_text_with_cursor()
        else:
            if len(self.value) == 0:
                text = self.placeholder
            else:
                text = Text(self.value)

        return self.render_panel(text)

    def render_panel(self, text: TextType) -> RenderableType:
        """
        Builds a panel for the Inpux Box
        """

        return Panel(
            text[self.view.start : self.view.end],
            title=self.title,
            title_align=self.title_align,
            height=3,
            border_style=("bold " if self.has_focus else "dim ")
            + str(self.border_style),
            box=SQUARE,
        )

    def _render_text_with_cursor(self) -> Text:
        """
        Produces renderable Text object combining value and cursor
        """

        text = Text()

        if self.password:
            text.append("•" * self._cursor_position)
            text.append(self.cursor, style="bold")
            text.append("•" * (len(self.value) - self._cursor_position))
        else:
            text.append(self.value[: self._cursor_position])
            text.append(self.cursor, style="bold")
            text.append(self.value[self._cursor_position :])

        return text

    async def on_focus(self, _: events.Focus) -> None:
        self._has_focus = True

    async def on_blur(self, _: events.Blur) -> None:
        self._has_focus = False

    def clear(self) -> None:
        """
        Clears the Input Box
        """
        self.value = ""
        self._cursor_position = 0
        self.refresh()

    def _is_allowed(self, text: str) -> bool:
        if self.list[0] == "whitelist":
            for letter in text:
                if letter not in self.list[1]:
                    return False
        else:
            for letter in text:
                if letter in self.list[1]:
                    return False

        return True

    async def _insert_text(self, text: str | None = None) -> None:
        """
        Inserts text where the cursor is
        """

        # Will throw an error if `xclip` if not installed on the linux(Xorg) system,
        # should work just fine on windows and mac

        if text is None:
            text = pyperclip.paste()

        if not self._is_allowed(text):
            await self.emit(InvalidInputAttempt(self))
            return

        self.value = (
            self.value[: self._cursor_position]
            + text
            + self.value[self._cursor_position :]
        )

        self._cursor_position += len(text)

    async def on_key(self, event: events.Key) -> None:
        """Send the key to the Input"""
        await self.keypress(event.key)

    async def _move_cursor_backward(self, word=False, delete=False) -> None:
        """
        Moves the cursor backwards..
        Optionally jumps over a word when pressed ctrl+left
        Optionally deletes the letter in case of backspace
        """

        prev = self._cursor_position

        if not word:
            self._cursor_position = max(self._cursor_position - 1, 0)
        else:
            while self._cursor_position:
                if self.value[self._cursor_position - 1] != " " and (
                    self._cursor_position == 1
                    or self.value[self._cursor_position - 2] == " "
                ):
                    self._cursor_position -= 1
                    break

                self._cursor_position -= 1

        if delete:
            self.value = self.value[: self._cursor_position] + self.value[prev:]

    async def _move_cursor_forward(self, word=False, delete=False) -> None:
        """
        Moves the cursor forward..
        Optionally jumps over a word when pressed ctrl+right
        Optionally deletes the letter in case of del or ctrl+del
        """

        prev = self._cursor_position

        if not word:
            self._cursor_position = min(self._cursor_position + 1, len(self.value))
        else:

            while self._cursor_position < len(self.value):
                if (
                    self._cursor_position != prev
                    and self.value[self._cursor_position - 1] == " "
                    and (
                        self._cursor_position == len(self.value) - 1
                        or self.value[self._cursor_position] != " "
                    )
                ):
                    break

                self._cursor_position += 1

        if delete:
            self.value = self.value[:prev] + self.value[self._cursor_position :]
            self._cursor_position = prev  # Because the cursor never actually moved :)

    def update_view(self, prev: int, curr: int) -> None:
        """
        Updates the current view-able part of the text if there is an overflow
        """

        if prev >= self.view.start and curr < self.view.start:
            self.view.start = curr

        elif prev <= self.view.end and curr >= self.view.end:
            self.view.start = max(0, curr - self.size.width + 5)

        self.view.end = self.view.start + self.size.width - 4

    async def keypress(self, key: str) -> None:
        """
        Handles Keypresses
        """
        prev = self._cursor_position

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
                self._cursor_position = 0

            case "end":
                self._cursor_position = len(self.value)

            # COPY-PASTA
            case "ctrl+v":
                try:
                    await self._insert_text()
                except:
                    await self.emit(PyperclipError(self))
                    return

        if len(key) == 1:
            await self._insert_text(key)

        self.update_view(prev, self._cursor_position)
        await self.emit(TextChanged(self))
        self.refresh()
