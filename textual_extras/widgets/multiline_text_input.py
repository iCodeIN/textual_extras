from rich.console import RenderableType
from rich.tree import Tree
from textual import events
from rich.panel import Panel
from .single_level_tree_edit import SingleLevelTreeEdit


class MultiLineTextInput(SingleLevelTreeEdit):
    def __init__(
        self,
        name: str | None = None,
        panel: Panel = Panel(""),
    ) -> None:
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
            panel=panel,
        )

        self.editing = True

    def highlight(self, index: int) -> None:
        self.options[self.highlighted].on_blur()
        self.options[index].on_focus()

        option = self.options[index]
        option._cursor_position = min(self._cursor_column, len(option.value))

        super().highlight(index)

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
                rest = self.current_opt.value[self._cursor_column :]
                self.current_opt.value = self.current_opt.value[: self._cursor_column]
                self.add_option_below()
                self.current_opt.value += rest
            case _:
                await self.current_opt.on_key(event)
                text = self.current_opt.value
                if len(text) == self.size.width - 5:
                    self.add_option_below()

        self._cursor_column = self.current_opt._cursor_position
        self.refresh()

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for option in self.options:

            label = option.render()
            tree.add(label)

        self.panel.renderable = tree
        return self.panel
