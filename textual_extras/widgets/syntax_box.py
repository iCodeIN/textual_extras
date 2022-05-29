from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from . import MultiLineTextInput


class SyntaxBox(MultiLineTextInput):
    """
    Multiline Input but with syntax support
    """

    def __init__(
        self,
        syntax: str,
        theme: str = "monokai",
        name: str | None = None,
    ) -> None:
        super().__init__(name)
        self.syntax = syntax
        self.theme = theme

    def render(self) -> RenderableType:
        return Panel(self.render_tree())

    def render_custom_label(self, label: Text, is_highlighted: bool) -> Text:
        console = Console()
        syntax_obj = Syntax(str(label), self.syntax, theme=self.theme)

        with console.capture() as capture:
            console.print(syntax_obj)

        label = Text.from_ansi(capture.get())
        return label
