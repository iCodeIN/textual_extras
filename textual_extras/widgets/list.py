from rich.console import RenderableType
from rich.tree import Tree
from rich.panel import Panel
from rich.text import TextType, Text
from rich.style import StyleType
from textual.widget import Widget
from textual import events

from ..events import ListItemSelected


class List(Widget):
    """
    A simple list class to show the items in a list
    """

    def __init__(
        self,
        name: str | None = None,
        options: list[TextType] = [],
        other_option_style: StyleType = "",
        highlighted_option_style: StyleType = "bold green",
        pad: bool = True,
        rotate: bool = False,
        wrap: bool = True,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(name)
        self.options = options
        self.other_option_style = other_option_style
        self.highlighted_option_style = highlighted_option_style
        self.pad = pad
        self.panel = panel
        self.rotate = rotate
        self.wrap = wrap
        self.selected = 0

    def select(self, id: int) -> None:
        self.selected = id
        self.refresh(layout=True)

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

    async def on_key(self, event: events.Key) -> None:
        event.stop()

        match event.key:
            case "j" | "down":
                self.move_cursor_down()
            case "k" | "up":
                self.move_cursor_up()
            case "g" | "home":
                self.move_cursor_to_top()
            case "G" | "end":
                self.move_cursor_to_bottom()
            case "enter":
                await self.emit(ListItemSelected(self, self.options[self.selected]))

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        """
        Move the highlight along with mouse hover
        """
        self.select(event.style.meta.get("selected"))

    def add_option(self, option: TextType) -> None:
        self.options.append(option)
        self.refresh()

    def render(self) -> RenderableType:

        # 1 borders + 1 space padding on each side
        width = self.size.width - 4

        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for index, option in enumerate(self.options):
            if isinstance(option, str):
                option = Text(option)

            option.pad_right(width - len(option) - 1)
            option = Text(f" ") + option

            if self.wrap:
                option.plain = option.plain[:width]

            if index != self.selected:
                option.stylize(self.other_option_style)
            else:
                option.stylize(self.highlighted_option_style)

            meta = {
                "@click": f"click_label({index})",
                "selected": index,
            }
            option.apply_meta(meta)
            tree.add(option)

        self.panel.renderable = tree
        return self.panel

    async def action_click_label(self, id):
        self.select(id)
        await self.emit(ListItemSelected(self, self.options[self.selected]))
