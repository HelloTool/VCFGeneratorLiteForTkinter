from tkinter import Entry, Menu, TclError, Text
from tkinter.constants import SEL_FIRST
from typing import Literal

from vcf_generator_lite.utils.tkinter.menu import MenuCommand, MenuSeparator, load_menu_items


def boolean_to_state(state: bool) -> Literal["normal", "disabled"]:
    return "normal" if state else "disabled"


def state_to_boolean(state: Literal["normal", "disabled"]) -> bool:
    return state == "normal"


class TextContextMenu(Menu):
    master: Text | Entry

    def __init__(self, master: Text | Entry, **kw):
        super().__init__(master, tearoff=False, **kw)

    def is_selected(self):
        try:
            self.master.index(SEL_FIRST)
            return True
        except TclError:
            return False

    def show(self, x: int, y: int):
        self.master.focus()
        self.delete(0, "end")
        state_by_selected = boolean_to_state(self.is_selected())
        is_master_editable = state_to_boolean(self.master.cget("state"))
        if is_master_editable:
            load_menu_items(
                self,
                [
                    MenuCommand(
                        label="撤销(&U)",
                        command=lambda: self.master.event_generate("<<Undo>>"),
                    ),
                    MenuCommand(
                        label="重做(&R)",
                        command=lambda: self.master.event_generate("<<Redo>>"),
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label="剪切(&T)",
                        command=lambda: self.master.event_generate("<<Cut>>"),
                        state=state_by_selected,
                    ),
                ],
            )
        load_menu_items(
            self,
            [
                MenuCommand(
                    label="复制(&C)",
                    command=lambda: self.master.event_generate("<<Copy>>"),
                    state=state_by_selected,
                ),
            ],
        )
        if is_master_editable:
            load_menu_items(
                self,
                [
                    MenuCommand(
                        label="粘贴(&P)",
                        command=lambda: self.master.event_generate("<<Paste>>"),
                    ),
                    MenuCommand(
                        label="删除(&D)",
                        command=lambda: self.master.event_generate("<<Clear>>"),
                        state=state_by_selected,
                    ),
                ],
            )
        load_menu_items(
            self,
            [
                MenuSeparator(),
                MenuCommand(
                    label="全选(&A)",
                    command=lambda: self.master.event_generate("<<SelectAll>>"),
                ),
            ],
        )
        self.tk_popup(x, y)

    def bind_to_widget(self):
        self.master.bind("<<ContextMenu>>", lambda event: self.show(event.x_root, event.y_root), add="+")
