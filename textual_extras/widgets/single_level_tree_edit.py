from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType
from rich.tree import Tree
from textual.widget import Widget
from textual_extras.widgets.text_input import View

from . import TextInput


class SimpleInput(TextInput):
    """
    A simple text Input with no panel
    """

    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        super().__init__(name, placeholder="", box=None)


class SingleLevelTreeEdit(Widget):
    """
    An editable tree structure with no nests
    """

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
        self.editing = False
        self.options_temp = options
        self.setup_done = False
        self.highlight(-1)
        self._setup_preoptions()

    def _setup_preoptions(self) -> None:
        """
        Pre - setup the already provided options
        """

        self.options: list[SimpleInput] = []
        for option in self.options_temp:
            self.add_option_below()
            # SAFETY: current opt will always be there becuse of the above line
            self.current_opt.value = str(option)
            self.unfocus_option()

    def highlight(self, index: int) -> None:
        self.highlighted = max(-1, index)
        if self.highlighted != -1:
            self.current_opt = self.options[self.highlighted]
        else:
            self.current_opt = None

        self.refresh()

    def cursor_down(self) -> None:
        """
        Moves the highlight down
        """

        if self.rotate:
            self.highlight((self.highlighted + 1) % len(self.options))
        else:
            self.highlight(min(self.highlighted + 1, len(self.options) - 1))

    def move_cursor_up(self):
        """
        Moves the highlight up
        """
        if not self.options:
            self.highlighted = -1
            return

        if self.rotate:
            self.highlight(
                (self.highlighted - 1 + len(self.options)) % len(self.options)
            )
        else:
            self.highlight(max(self.highlighted - 1, 0))

    def move_to_top(self) -> None:
        """
        Moves the cursor to the top
        """
        self.highlight(0)

    def move_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.highlight(len(self.options) - 1)

    def remove_option(self, index: int | None = None) -> None:
        index = index or self.highlighted
        self.options.pop(self.highlighted)
        self.move_cursor_up()

    def add_option_below(self, move_cursor: bool = True) -> None:
        self.options.insert(self.highlighted + 1, SimpleInput())
        if move_cursor:
            self.cursor_down()
            self.focus_option()

    def add_option_at_end(self, edit: bool = True) -> None:
        self.options.insert(len(self.options), SimpleInput())
        if edit:
            self.move_to_bottom()
            self.focus_option()

    def add_option(self, index: int, edit: bool = True) -> None:
        self.options.insert(index, SimpleInput())
        if edit:
            self.highlight(index)
            self.focus_option()

    def focus_option(self) -> None:
        if self.current_opt:
            self.current_opt.on_focus()
        self.editing = True
        self.refresh()

    def unfocus_option(self) -> None:
        if self.current_opt:
            self.current_opt.on_blur()
        self.editing = False
        self.refresh()

    def render(self) -> RenderableType:

        if not self.setup_done:
            self.setup_done = True

        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True
        width = self.size.width - 4

        for index, option in enumerate(self.options):

            if not hasattr(option, "view"):
                option.view = View(0, width - 1)

            label = Text(str(option.view))
            label = option.render()
            label = Text(" ") + label
            label.pad_right(width)

            if self.wrap:
                label = label[: self.size.width - 4]

            if index == self.highlighted:
                if self.editing:
                    label.stylize(self.style_editing)
                else:
                    label.stylize(self.style_focused)
            else:
                label.stylize(self.style_unfocused)

            tree.add(label)

        self.panel.renderable = tree
        return self.panel
