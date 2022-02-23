from rich.text import Text
import pyperclip

from .text_input import TextInput


class NumberInput(TextInput):
    def _insert_text(self, text: str | None = None) -> None:
        """
        Inserts text where the cursor is
        """

        # Will throw an error if `xclip` if not installed on the system
        if text is None:
            text = pyperclip.paste()

        for letter in text:
            if not (letter.isdigit() or letter == " "):
                return

        self.value = (
            self.value[: self._cursor_position]
            + text
            + self.value[self._cursor_position :]
        )
        self._cursor_position += len(text)


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                NumberInput(
                    title="text",
                    title_align="left",
                    placeholder=Text("Enter yo message...", style="dim white"),
                )
            )

    MyApp.run()
