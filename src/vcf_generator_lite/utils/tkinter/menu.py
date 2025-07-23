from abc import ABC
from collections.abc import Callable
from dataclasses import dataclass
from tkinter import Menu
from typing import Self, Literal

from vcf_generator_lite.utils.tkinter.window import WindowExtension


@dataclass
class MenuCommand:
    label: str
    command: Callable[[], object | str] | None = None
    accelerator: str | None = None
    state: Literal["normal", "active", "disabled"] = "normal"


@dataclass
class MenuSeparator:
    pass


@dataclass
class MenuCascade:
    label: str
    items: list[MenuCommand | MenuSeparator | Self | type[MenuSeparator]]
    accelerator: str | None = None
    tearoff: bool = False
    state: Literal["normal", "active", "disabled"] = "normal"


type MenuItem = MenuCommand | MenuSeparator | MenuCascade | type[MenuSeparator]


def _parse_label(label: str) -> tuple[str, int]:
    """
    解析标签字符串，将标签字符串中的快捷键标识符替换为对应的快捷键键值
    """
    return label.replace("&", "", 1), label.find("&")


def add_menu_items(menu: Menu, items: list[MenuItem]):
    """
    向给定的菜单对象中批量添加菜单项。
    """
    for item in items:
        if isinstance(item, MenuCommand):
            label, underline = _parse_label(item.label)
            menu.add_command(
                label=label,
                command=item.command,  # pyright: ignore[reportArgumentType]
                underline=underline,
                accelerator=item.accelerator,  # pyright: ignore[reportArgumentType]
                state=item.state,
            )
        elif isinstance(item, MenuSeparator) or (type(item) == type and issubclass(item, MenuSeparator)):
            menu.add_separator()
        elif isinstance(item, MenuCascade):
            label, underline = _parse_label(item.label)
            submenu = Menu(menu, tearoff=item.tearoff)
            add_menu_items(submenu, item.items)
            menu.add_cascade(
                label=label,
                menu=submenu,
                underline=underline,
                accelerator=item.accelerator,  # pyright: ignore[reportArgumentType]
                state=item.state,
            )


class MenuBarWindowExtension(WindowExtension, ABC):
    menu_bar: Menu | None = None

    def add_menu_bar_items(self, *items: MenuItem):
        if self.menu_bar is None:
            self.menu_bar = Menu(self, tearoff=False)
            self.configure({"menu": self.menu_bar})
        add_menu_items(self.menu_bar, list(items))
