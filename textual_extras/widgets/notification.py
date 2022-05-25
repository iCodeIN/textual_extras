from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType
from textual import events
from textual.widget import Widget


class Notification(Widget):
    def __init__(
        self,
        name: str | None = None,
        message: TextType = "This is a notification",
        timeout: float = 5,
        panel: Panel = Panel(""),
        bar_style: StyleType = "bold blue",
    ) -> None:
        super().__init__(name)
        self.message = message
        self.timeout = timeout
        self.subtitle_length = 100
        self.started = False
        self.bar_style = bar_style
        self.panel = panel

    def _calculate_lines(self):
        width = self.size.width - 4
        lines = 1
        c = 0

        for i in self.message.split():
            if c + len(i) > width:
                lines += 1
                c = len(i) + 1
            else:
                c += len(i) + 1

        return lines

    async def popup(self):
        if not self.started:
            self.subtitle_length = self.size.width - 2
            self.started = True

            tick_rate = self.timeout / (self.subtitle_length)
            self.timer = self.set_interval(tick_rate, self.tick)

    def tick(self):
        if self.subtitle_length:
            self.subtitle_length -= 1
        else:
            self.timer.pause()
            self.started = False

        self.refresh()

    async def on_click(self, _: events.Click) -> None:
        self.started = False
        self.refresh()

    def render(self) -> RenderableType:
        if self.started:
            subtitle = Text(
                "━" * self.subtitle_length,
                style=self.bar_style,
            )
            subtitle.pad_right(self.size.width)

            self.panel.renderable = self.message
            self.panel.expand = False
            self.panel.subtitle = subtitle
            self.panel.height = self._calculate_lines() + 2
            self.panel.subtitle_align = "left"

            return self.panel
        else:
            return ""
