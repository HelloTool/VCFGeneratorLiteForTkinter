from tkinter import Tk
from tkinter.font import nametofont
from typing import override

from vcf_generator_lite.themes.base import BaseThemePatch


class DefaultThemePatch(BaseThemePatch):
    @override
    def __init__(self, app: Tk):
        super().__init__(app)

        default_font = nametofont("TkDefaultFont")
        default_font_size = int(default_font.actual("size"))

        # 重写部分配置以适配高分屏
        self.style.configure("TButton", padding="2.5p", width=-8)
        self.style.configure("Treeview", rowheight=f"{default_font_size + 6}p")
        self.style.configure("Heading", padding="2.25p")
        self.style.configure("Vertical.TScrollbar", arrowsize="9p")
