from textual import events
from rich.panel import Panel
from .single_level_tree_edit import SingleLevelTreeEdit


class MultiLineTextInput(SingleLevelTreeEdit):
    def __init__(
        self,
        name: str | None = None,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(
            name,
            options=[""],
            style_unfocused="",
            style_focused="",
            style_editing="",
            pad=True,
            rotate=False,
            wrap=False,
            panel=panel,
        )
        self._cursor_column = 0
        self.editing = True
        self.select(0)

    def select(self, index: int) -> None:
        self.options[self.selected].on_blur()
        self.options[index].on_focus()
        return super().select(index)

    async def on_key(self, event: events.Key) -> None:
        match event.key:
            case "up":
                self.move_cursor_up()
            case "down":
                self.move_cursor_down()
            case "ctrl+home":
                self.move_cursor_to_top()
            case "ctrl+end":
                self.move_cursor_to_bottom()
            case "enter":
                self.add_option_below()
            case _:
                await self.options[self.selected].handle_keypress(event.key)

        self.refresh()
