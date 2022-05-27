from rich.console import RenderableType
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.style import StyleType
from rich.text import Text, TextType
from textual import events
from textual.widgets import TreeControl, TreeNode, NodeID

from textual_extras.widgets.text_input import View

from . import SimpleInput

NodeDataType = SimpleInput


class NestedListEdit(TreeControl):
    def __init__(
        self,
        label: TextType,
        data: SimpleInput,
        name: str | None = None,
        padding: PaddingDimensions = (1, 1),
        style_unfocus: StyleType = "d white",
        style_focus: StyleType = "b blue",
        style_editing: StyleType = "b cyan",
        panel: Panel = Panel(""),
    ) -> None:
        self.nodes: dict[NodeID, TreeNode[SimpleInput]] = {}

        super().__init__(label, data, name=name, padding=padding)
        self._tree.hide_root = True
        self._tree.expanded = True
        self.style_focus = style_focus
        self.style_unfocus = style_unfocus
        self.style_editing = style_editing
        self.panel = panel
        self.editing = False
        self.highlight(self.root.id)

    def render(self):
        self.panel.renderable = self._tree
        return self.panel

    def highlight(self, id: NodeID):
        self.highlighted = id
        self.cursor = id
        self.refresh()

    def focus_node(self):
        self.nodes[self.highlighted].data.on_focus()
        self.editing = True

    def unfocus_node(self):
        self.nodes[self.highlighted].data.on_blur()
        self.editing = False

    async def key_down(self, _: events.Key) -> None:
        pass

    async def key_up(self, _: events.Key) -> None:
        pass

    async def cursor_down(self) -> None:
        node = self.nodes[self.highlighted]

        if next_node := node.next_node:
            self.highlight(next_node.id)
        elif node == self.root:
            if node.children:
                self.highlight(node.children[0].id)
        else:
            return

        self.cursor_line += 1

    async def cursor_up(self) -> None:
        next_node = self.nodes[self.highlighted]

        if next_node := next_node.previous_node:
            if next_node != self.root:
                self.highlight(next_node.id)
                self.cursor_line += 1

    async def move_to_top(self):
        if children := self.root.children:
            self.highlight(children[0].id)

    async def move_to_bottom(self):
        if children := self.root.children:
            self.highlight(children[-1].id)

    async def toggle_expand(self):
        if self.highlighted != self.root.id:
            await self.nodes[self.highlighted].toggle()

    async def toggle_expand_parent(self):
        if (
            self.highlighted != self.root.id
            and self.nodes[self.highlighted].parent != self.root
        ):
            await self.reach_to_parent()
            await self.nodes[self.highlighted].toggle()

    async def reach_to_parent(self):
        if parent := self.nodes[self.highlighted].parent:
            while self.highlighted != parent.id:
                await self.cursor_up()

    async def reach_to_last_child(self):
        if children := self.nodes[self.highlighted].children:
            while self.highlighted != children[-1].id:
                await self.cursor_down()

    async def add_child(self):
        node = self.nodes[self.highlighted]
        await node.add("child", SimpleInput())
        await node.expand()
        await self.reach_to_last_child()
        self.focus_node()

    async def add_sibling(self):
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", SimpleInput())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()
        self.focus_node()

    async def send_key_to_selected(self, event: events.Key):
        await self.nodes[self.highlighted].data.on_key(event)

    async def on_key(self, event: events.Key):
        if self.editing:
            match event.key:
                case "escape":
                    self.unfocus_node()
                case _:
                    await self.send_key_to_selected(event)

        else:
            match event.key:
                case "j" | "down":
                    await self.cursor_down()
                case "k" | "up":
                    await self.cursor_up()
                case "g":
                    await self.move_to_top()
                case "G":
                    await self.move_to_bottom()
                case "z":
                    await self.toggle_expand()
                case "Z":
                    await self.toggle_expand_parent()
                case "A":
                    await self.add_child()
                case "a":
                    await self.add_sibling()
                case "i":
                    self.focus_node()

        self.refresh()

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        """
        Move the highlight along with mouse hover
        """
        if not self.editing:
            if id := event.style.meta.get("tree_node"):
                self.highlight(id)

    def render_node(self, node: TreeNode) -> RenderableType:

        if not hasattr(node.data, "view"):
            node.data.view = View(0, self.size.width - 6)

        return self.render_custom_node(node)

    def render_custom_node(self, node) -> RenderableType:

        label = (
            Text(str(node.data.render()), no_wrap=True)
            if isinstance(node.label, str)
            else node.label
        )
        label.pad_right(self.size.width)

        if node.id == self.highlighted:
            label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
        }

        label.apply_meta(meta)
        return label

    async def handle_tree_click(self, _) -> None:
        if not self.editing:
            self.focus_node()
