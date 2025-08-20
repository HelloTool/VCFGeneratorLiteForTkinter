from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import Menu
from typing import Literal, TypedDict, override

from vcf_generator_lite.utils.tkinter.window import WindowExtension


class MenuItem(ABC):
    @abstractmethod
    def load(self, menu: Menu): ...


@dataclass
class MenuCommand(MenuItem):

    label: str
    command: Callable[[], object | str] | None = None
    accelerator: str | None = None
    state: Literal["normal", "active", "disabled"] = "normal"

    @override
    def load(self, menu: Menu):
        menu.add_command(
            command=self.command,  # pyright: ignore[reportArgumentType]
            accelerator=self.accelerator,  # pyright: ignore[reportArgumentType]
            state=self.state,
            **_parse_label(self.label),
        )


@dataclass
class MenuSeparator(MenuItem):

    @override
    def load(self, menu: Menu):
        menu.add_separator()


@dataclass
class MenuCascade(MenuItem):
    label: str
    items: list[MenuItem]
    accelerator: str | None = None
    tearoff: bool = False
    state: Literal["normal", "active", "disabled"] = "normal"

    @override
    def load(self, menu: Menu):
        submenu = Menu(menu, tearoff=self.tearoff)
        load_menu_items(submenu, self.items)
        menu.add_cascade(
            menu=submenu,
            accelerator=self.accelerator,  # pyright: ignore[reportArgumentType]
            state=self.state,
            **_parse_label(self.label),
        )


class ParseLabelResult(TypedDict):
    label: str
    underline: int


def _parse_label(label: str) -> ParseLabelResult:
    """
    解析标签字符串，将标签字符串中的快捷键标识符设置为对应的快捷键键值
    """

    return ParseLabelResult(label=label.replace("&", "", 1), underline=label.find("&"))


def load_menu_items(menu: Menu, items: list[MenuItem]):
    for item in items:
        item.load(menu)


class MenuBarWindowExtension(WindowExtension, ABC):
    menu_bar: Menu | None = None

    def load_menu_bar_items(self, *items: MenuItem):
        if self.menu_bar is None:
            self.menu_bar = Menu(self, tearoff=False)
            self.configure({"menu": self.menu_bar})
        load_menu_items(self.menu_bar, list(items))
