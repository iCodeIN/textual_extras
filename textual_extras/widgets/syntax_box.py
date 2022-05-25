from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree
from . import MultiLineTextInput


class SyntaxBox(MultiLineTextInput):
    def __init__(
        self,
        syntax: str,
        theme: str = "monokai",
        name: str | None = None,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(name, panel)
        self.syntax = syntax
        self.theme = theme

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for option in self.options:

            label = option.render()

            CONSOLE = Console()
            syntax_obj = Syntax(str(label), self.syntax, theme=self.theme)

            with CONSOLE.capture() as capture:
                CONSOLE.print(syntax_obj)

            label = Text.from_ansi(capture.get())
            tree.add(label)

        self.panel.renderable = tree
        return self.panel
