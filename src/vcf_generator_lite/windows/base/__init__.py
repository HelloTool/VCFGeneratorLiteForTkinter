import logging
from abc import ABC
from tkinter import PhotoImage, Tk, Toplevel, Wm
from typing import override

from vcf_generator_lite.themes import create_theme_patch
from vcf_generator_lite.themes.abs import ThemePatch
from vcf_generator_lite.utils import resources
from vcf_generator_lite.utils.tkinter.misc import ScalingMiscExtension
from vcf_generator_lite.utils.tkinter.window import (
    CenterWindowExtension,
    GeometryWindowExtension,
    WindowExtension,
    withdraw_cm,
)
from vcf_generator_lite.windows.base.constants import EVENT_ENHANCED_THEME_CHANGED, EVENT_EXIT

__all__ = ["ExtendedTk", "ExtendedToplevel", "ExtendedDialog"]
_logger = logging.getLogger(__name__)


class AppWindowExtension(
    GeometryWindowExtension,
    ScalingMiscExtension,
    CenterWindowExtension,
    WindowExtension,
    ABC,
):
    """
    应用程序窗口扩展基类，集成多个窗口功能扩展

    特性：
    - 继承 GeometryWindowExtension: 提供基于物理/虚拟像素的窗口尺寸控制
    - 继承 ScalingWindowExtension: 支持高DPI屏幕的自适应缩放
    - 继承 CenterWindowExtension: 实现窗口居中显示功能
    - 继承 WindowExtension: 基础窗口功能扩展
    """

    def __init__(self):
        super().__init__()
        with withdraw_cm(self):
            self._configure_ui_withdraw()
            self.update_idletasks()  # 在deiconify前调用可以一定程度上防止首次启动时窗口闪烁
        self._configure_ui()

    def _configure_ui_withdraw(self):
        self.__apply_default_events()

    def _configure_ui(self):
        self.center()

    def __apply_default_events(self):
        self.protocol("WM_DELETE_WINDOW", lambda: self.event_generate(EVENT_EXIT))
        self.bind(EVENT_EXIT, lambda _: self.destroy())


class ExtendedTk(Tk, AppWindowExtension, ABC):
    theme_patch: ThemePatch

    def __init__(self, **kw):
        super().__init__(baseName="vcf_generator_lite", **kw)
        AppWindowExtension.__init__(self)

    @override
    def _configure_ui_withdraw(self):
        self.apply_theme_patch()
        super()._configure_ui_withdraw()
        self.__apply_default_icon()

    def __apply_default_icon(self):
        self.iconphoto(True, PhotoImage(master=self, data=resources.read_binary("images/icon-48.png")))

    def apply_theme_patch(self):
        self.theme_patch = create_theme_patch(self)
        self.theme_patch.configure_window(self)
        self.event_generate(EVENT_ENHANCED_THEME_CHANGED)


class ExtendedToplevel(Toplevel, AppWindowExtension, ABC):
    def __init__(self, master: Tk | Toplevel, **kw):
        super().__init__(master, **kw)
        AppWindowExtension.__init__(self)

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.__apply_theme()

    def __apply_theme(self):
        root: ExtendedTk = self.nametowidget(".")
        root.theme_patch.configure_window(self)
        root.bind(EVENT_ENHANCED_THEME_CHANGED, lambda _: root.theme_patch.configure_window(self))


class ExtendedDialog(ExtendedToplevel, ABC):

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.bind("<Escape>", lambda _: self.event_generate(EVENT_EXIT))

        if isinstance(self.master, Wm):
            self.transient(self.master)
            self.resizable(False, False)
