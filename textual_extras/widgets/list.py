from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Span, TextType, Text
from rich.style import StyleType
from textual.widget import Widget
from textual import events

from ..events import ListItemSelected


class List(Widget):
    """
    A simple list class to show the items in a list (No Mouse Support: Consider List2)
    """

    def __init__(
        self,
        name: str | None = None,
        options: list[TextType] = [],
        other_option_style: StyleType = "",
        highlighted_option_style: StyleType = "bold green",
        pad: bool = True,
        rotate: bool = False,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(name)
        self.options = options
        self.other_option_style = other_option_style
        self.highlighted_option_style = highlighted_option_style
        self.pad = pad
        self.panel = panel
        self.rotate = rotate
        self.selected = 0

    def render_panel(self, renderable: Text) -> RenderableType:
        """
        Renders the list with specified panel
        """
        width = self.size.width - 2
        start = self.selected * width
        end = start + width

        renderable.spans.append(Span(start, end, self.highlighted_option_style))
        self.panel.renderable = renderable

        return self.panel

    def move_cursor_down(self) -> None:
        """
        Moves the highlight down
        """

        if self.rotate:
            self.selected = (self.selected + 1) % len(self.options)
        else:
            self.selected = min(self.selected + 1, len(self.options) - 1)

        self.refresh()

    def move_cursor_up(self):
        """
        Moves the highlight up
        """

        if self.rotate:
            self.selected = (self.selected - 1 + len(self.options)) % len(self.options)
        else:
            self.selected = max(self.selected - 1, 0)

        self.refresh()

    def move_cursor_to_top(self) -> None:
        """
        Moves the cursor to the top
        """

        self.selected = 0
        self.refresh()

    def move_cursor_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.selected = len(self.options) - 1
        self.refresh()

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

    def render(self) -> RenderableType:
        width = self.size.width - 3
        renderable = Text()

        for index, option in enumerate(self.options):
            if isinstance(option, str):
                option = Text(option)

            option.pad_right(width - len(option) - 1)
            option = Text(" ") + option
            option = option[:width]

            if index != self.selected:
                option.stylize(self.other_option_style)

            renderable.append("\n")
            renderable.append(option)

        return self.render_panel(renderable)
