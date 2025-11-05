from abc import ABC
from tkinter import Tk, Toplevel
from tkinter.ttk import Style
from typing import override

from vcf_generator_lite.themes.abs import ThemePatch


class BaseThemePatch(ThemePatch, ABC):
    style: Style

    def __init__(self, app: Tk):
        self.style = Style(app)
        # 防止编辑框将其他组件挤出窗口
        app.option_add("*ThemedText.Text.width", 0, "startupFile")
        app.option_add("*ThemedText.Text.height", 0, "startupFile")

    @override
    def configure_window(self, master: Tk | Toplevel):
        window_background: str = self.style.lookup("TFrame", "background")
        master.configure(background=window_background)
