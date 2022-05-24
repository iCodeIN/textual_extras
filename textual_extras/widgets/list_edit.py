from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType
from rich.tree import Tree
from textual import events
from textual.widget import Widget

from . import TextInput
from ..events import ListItemSelected


class SimpleInput(TextInput):
    def _format_text(self, text: str) -> str:
        # why? there is no width to determine the view
        return text

    def render_panel(self, text: TextType) -> RenderableType:
        return text


class ListEdit(Widget):
    def __init__(
        self,
        name: str | None = None,
        options: list[TextType] = [],
        style_unfocused: StyleType = "",
        style_focused: StyleType = "bold green",
        style_editing: StyleType = "bold cyan",
        pad: bool = True,
        rotate: bool = False,
        wrap: bool = True,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(name)
        self.style_unfocused = style_unfocused
        self.style_focused = style_focused
        self.style_editing = style_editing
        self.pad = pad
        self.panel = panel
        self.rotate = rotate
        self.wrap = wrap
        self.selected = 0
        self.editing = False
        self.pre_setup_options(options)

    def pre_setup_options(self, options: list[TextType]):
        self.options: list[SimpleInput] = []
        for option in options:
            a = SimpleInput(box=None)
            if isinstance(option, str):
                option = Text(option)

            a.value = option.plain
            a._cursor_position = len(a.value)

            self.options.append(a)

    def select(self, index: int) -> None:
        self.selected = index
        self.refresh()

    def move_cursor_down(self) -> None:
        """
        Moves the highlight down
        """

        if self.rotate:
            self.select((self.selected + 1) % len(self.options))
        else:
            self.select(min(self.selected + 1, len(self.options) - 1))

    def move_cursor_up(self):
        """
        Moves the highlight up
        """

        if self.rotate:
            self.select((self.selected - 1 + len(self.options)) % len(self.options))
        else:
            self.select(max(self.selected - 1, 0))

    def move_cursor_to_top(self) -> None:
        """
        Moves the cursor to the top
        """
        self.select(0)

    def move_cursor_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.select(len(self.options) - 1)

    def focus_option(self):
        self.options[self.selected].on_focus()
        self.editing = True
        self.refresh()

    def unfocus_option(self):
        self.options[self.selected].on_blur()
        self.editing = False
        self.refresh()

    async def on_key(self, event: events.Key) -> None:
        event.stop()

        if self.editing:
            if event.key == "escape":
                self.unfocus_option()
            else:
                await self.options[self.selected].on_key(event)

        else:
            match event.key:
                case "j" | "down":
                    self.move_cursor_down()
                case "k" | "up":
                    self.move_cursor_up()
                case "g" | "home":
                    self.move_cursor_to_top()
                case "G" | "end":
                    self.move_cursor_to_bottom()
                case "i":
                    self.focus_option()
                case "enter":
                    await self.emit(
                        ListItemSelected(
                            self,
                            self.options[self.selected].value,
                        )
                    )

        self.refresh()

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        width = self.size.width - 4

        for index, option in enumerate(self.options):
            # SAFETY: It will always return text type..
            # since the box is set to None
            label = Text.from_markup(option.render())
            label = Text(" ") + label
            label.pad_right(width)

            if self.wrap:
                label = label[: self.size.width - 4]

            if index == self.selected:
                if self.editing:
                    label.stylize(self.style_editing)
                else:
                    label.stylize(self.style_focused)
            else:
                label.stylize(self.style_unfocused)

            tree.add(label)

        self.panel.renderable = tree
        return self.panel
