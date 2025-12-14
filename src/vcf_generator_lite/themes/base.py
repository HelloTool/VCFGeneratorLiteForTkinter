from abc import ABC
from tkinter import Tk
from tkinter.ttk import Style

from vcf_generator_lite.themes.abs import ThemePatch


class BaseThemePatch(ThemePatch, ABC):
    style: Style

    def __init__(self, app: Tk):
        self.style = Style(app)
        # 防止编辑框将其他组件挤出窗口
        app.option_add("*ThemedText.Text.width", 0, "startupFile")
        app.option_add("*ThemedText.Text.height", 0, "startupFile")
