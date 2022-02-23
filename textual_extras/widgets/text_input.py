from rich.box import SQUARE, DOUBLE
from rich.align import AlignMethod
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType

from textual import events
from textual.reactive import Reactive
from textual.widget import Widget
from rich.console import RenderableType

import pyperclip


class SingleLineInput(Widget):
    """
    A simple text input widget.
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
        value: str = "",
        placeholder: TextType = Text("Speak your mind ..", style="dim white"),
        password: bool = False,
    ) -> None:
        super().__init__(name)
        self.value = value
        self.title = title
        self.title_align: AlignMethod = title_align  # Silence compiler warning
        self.border_style: StyleType = border_style
        self.placeholder = placeholder
        self.password = password
        self._cursor_position = len(self.value)

    @property
    def has_focus(self) -> bool:
        return self._has_focus

    def render(self) -> RenderableType:
        if self.has_focus:
            text = self._render_text_with_cursor()
        else:
            if len(self.value) == 0:
                text = self.placeholder
            else:
                text = Text(self.value)

        return Panel(
            text,
            title=self.title,
            title_align=self.title_align,
            height=3,
            border_style=self.border_style,
            box=DOUBLE if self.has_focus else SQUARE,
        )

    def _render_text_with_cursor(self) -> Text:
        """
        Produces the renderable Text object combining value and cursor
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

    def clear(self):
        self.value = ""
        self._cursor_position = 0
        self.refresh()

    def _insert_text(self, text: str | None = None) -> None:
        try:
            # Will throw an error if `xclip` if not installed on the system
            if text is None:
                text = pyperclip.paste()

            self.value = (
                self.value[: self._cursor_position]
                + text
                + self.value[self._cursor_position :]
            )
            self._cursor_position += len(text)
        except:
            pass

    async def on_key(self, event: events.Key):
        await self.keypress(event.key)

    async def keypress(self, key: str) -> None:
        match key:
            case "left":
                self._cursor_position = max(self._cursor_position - 1, 0)

            case "right":
                self._cursor_position = min(self._cursor_position + 1, len(self.value))

            case "home":
                self._cursor_position = 0

            case "end":
                self._cursor_position = len(self.value)

            case "ctrl+h":  # Backspace
                if self._cursor_position:
                    self._cursor_position = max(self._cursor_position - 1, 0)
                    self.value = (
                        self.value[: self._cursor_position]
                        + self.value[self._cursor_position + 1 :]
                    )

            case "delete":
                self.value = (
                    self.value[: self._cursor_position]
                    + self.value[self._cursor_position + 1 :]
                )

            case "ctrl+v":
                self._insert_text()

        if len(key) == 1:
            self._insert_text(key)

        self.refresh()


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                SingleLineInput(
                    title="text",
                    title_align="left",
                    placeholder=Text("Enter yo message...", style="dim white"),
                )
            )

    MyApp.run()
