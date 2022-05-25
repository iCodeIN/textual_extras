from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType
from rich.tree import Tree
from textual import events

from textual_extras.events.events import ListItemSelected

from .single_level_tree_edit import SingleLevelTreeEdit
from .text_input import TextInput, View


class SearchList(SingleLevelTreeEdit):
    def __init__(
        self,
        name: str | None = None,
        options: list[TextType] = [],
        style_unfocused: StyleType = "",
        style_focused: StyleType = "bold green",
        style_search_match: StyleType = "bold red",
        style_editing: StyleType = "bold cyan",
        pad: bool = True,
        rotate: bool = False,
        wrap: bool = True,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(
            name,
            options,
            style_unfocused,
            style_focused,
            style_editing,
            pad,
            rotate,
            wrap,
            panel,
        )

        self.style_search_match = style_search_match
        self.search_box = TextInput(
            placeholder=Text(
                "Search here ...",
                style="dim white",
            )
        )
        self.option_copy = self.options[:]
        self.search_box.view = View(0, 100)
        self.search_mode = False

    def start_search(self):
        self.search_mode = True
        self.search_box.on_focus()
        self.option_copy = self.options[:]

    def stop_search(self):
        self.search_mode = False
        self.search_box.on_blur()

        if not self.search_box.value:
            self.options = self.option_copy[:]

    async def clear_search_box(self):
        while self.search_box.value:
            await self.search_box.handle_keypress("ctrl+h")

        if self.option_copy:
            self.selected = 0
        else:
            self.selected = None

        self.options = self.option_copy[:]

    async def on_key(self, event: events.Key) -> None:

        if self.search_mode:
            if event.key == "escape":
                self.stop_search()
            else:
                await self.search_box.handle_keypress(event.key)
                if self.search_box.value:
                    search = self.search_box.value
                    if [i for i in self.option_copy[:] if search in i.value]:
                        self.selected = 0
                    else:
                        self.selected = None
                else:
                    await self.clear_search_box()

        elif self.editing:
            match event.key:
                case "escape":
                    self.unfocus_option()
                case "ctrl+l":
                    await self.clear_search_box()
                case _:
                    if self.selected is not None:
                        await self.options[self.selected].handle_keypress(event.key)

        else:

            match event.key:
                case "ctrl+s":
                    self.start_search()
                case "ctrl+l":
                    await self.clear_search_box()
                case _:
                    if self.selected is None:
                        return

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
                        case "a":
                            self.add_option_below()
                        case "A":
                            self.add_option_at_end()
                        case "enter":
                            if self.selected is not None:
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
        search = self.search_box.value

        tree.add(self.search_box.render())
        self.options = [i for i in self.option_copy[:] if search in i.value]

        for index, option in enumerate(self.options):

            label = option.render()

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

            label.highlight_regex(search, style=self.style_search_match)
            tree.add(label)

        self.panel.renderable = tree
        return self.panel