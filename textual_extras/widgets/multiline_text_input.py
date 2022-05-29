from textual import events
from .single_level_tree_edit import SingleLevelTreeEdit


class MultiLineTextInput(SingleLevelTreeEdit):
    def __init__(self, name: str | None = None) -> None:
        self._cursor_column = 0

        super().__init__(
            name,
            options=[""],
            style_unfocused="",
            style_focused="",
            style_editing="",
            pad=True,
            rotate=False,
            wrap=False,
        )

        self.editing = True
        self.highlight(0)

    def highlight(self, index: int) -> None:

        if hasattr(self, "options"):
            self.options[self.highlighted].on_blur()
            self.options[index].on_focus()

            option = self.options[index]
            option._cursor_position = min(self._cursor_column, len(option.value))

        super().highlight(index)

    async def on_key(self, event: events.Key) -> None:
        match event.key:
            case "up":
                self.cursor_up()
            case "down":
                self.cursor_down()
            case "ctrl+home":
                self.move_to_top()
            case "ctrl+end":
                self.move_to_bottom()
            case "enter":
                if self.current_opt:
                    rest = self.current_opt.value[self._cursor_column :]
                    self.current_opt.value = self.current_opt.value[
                        : self._cursor_column
                    ]
                    self.add_option_below()
                    self.current_opt.value += rest
            case _:
                if self.current_opt:
                    await self.current_opt.on_key(event)
                    text = self.current_opt.value
                    if len(text) == self.size.width - 5:
                        self.add_option_below()

        if self.current_opt:
            self._cursor_column = self.current_opt._cursor_position

        self.refresh()
