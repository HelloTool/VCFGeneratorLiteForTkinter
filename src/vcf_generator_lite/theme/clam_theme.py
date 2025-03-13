from tkinter import Tk, Misc
from tkinter.ttk import Style
from typing import override

from vcf_generator_lite.theme.base import BaseTheme


class ClamTheme(BaseTheme):
    @override
    def apply_theme(self, master: Misc, style: Style):
        super().apply_theme(master, style)
        style.theme_use("clam")

        # 重写部分配置以适配高分屏
        style.configure("TButton", padding="2.5p")
        style.configure("Treeview", rowheight="15p")
        style.configure("Heading", padding="2.25p")
        style.configure("Vertical.TScrollbar", arrowsize="9p")

        # 自定义组件
        style.configure("DialogHeader.TFrame", relief="raised")
        style.configure("TextFrame.TEntry", padding=0, borderwidth="1.5p")

        # 窗口背景色不会跟随主题变化，需要手动设置
        window_background = style.lookup("TFrame", "background")
        if isinstance(master, Tk):
            master.configure(background=window_background)
        master.option_add("*Toplevel.background", window_background)
