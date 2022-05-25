from textual import events

from . import SingleLevelTreeEdit
from ..events import ListItemSelected


class ListEdit(SingleLevelTreeEdit):
    async def on_key(self, event: events.Key) -> None:
        if self.editing:
            if event.key == "escape":
                self.unfocus_option()
            else:
                await self.options[self.selected].handle_keypress(event.key)

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
                case "a":
                    self.add_option_below()
                case "A":
                    self.add_option_at_end()
                case "x":
                    self.remove_option()
                case "enter":
                    await self.emit(
                        ListItemSelected(
                            self,
                            self.options[self.selected].value,
                        )
                    )

        self.refresh()
