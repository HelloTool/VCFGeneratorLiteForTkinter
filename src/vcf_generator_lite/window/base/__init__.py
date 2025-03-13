import logging
from abc import ABC, abstractmethod
from tkinter import PhotoImage, Tk, Toplevel, Wm
from tkinter.ttk import Style
from typing import override

from vcf_generator_lite import resources
from vcf_generator_lite.theme import create_platform_theme
from vcf_generator_lite.util.tkinter.misc import ScalingMiscExtension
from vcf_generator_lite.util.tkinter.theme import Theme
from vcf_generator_lite.util.tkinter.window import CenterWindowExtension, GeometryWindowExtension, \
    WindowExtension, withdraw_cm, GcWindowExtension
from vcf_generator_lite.window.base.constants import EVENT_EXIT

__all__ = ["ExtendedTk", "ExtendedToplevel", "ExtendedDialog"]

logger = logging.getLogger(__name__)


class AppWindowExtension(GcWindowExtension, GeometryWindowExtension, ScalingMiscExtension, CenterWindowExtension,
                         WindowExtension, ABC):
    """
    应用程序窗口扩展基类，集成多个窗口功能扩展

    特性：
    - 继承 GeometryWindowExtension: 提供基于物理/虚拟像素的窗口尺寸控制
    - 继承 ScalingWindowExtension: 支持高DPI屏幕的自适应缩放
    - 继承 CenterWindowExtension: 实现窗口居中显示功能
    - 继承 WindowExtension: 基础窗口功能扩展
    - 抽象类要求子类必须实现 on_init_window 方法
    """

    def __init__(self):
        super().__init__()
        self.__apply_default_icon()
        self.__apply_default_events()
        self.on_init_window()

    @abstractmethod
    def on_init_window(self):
        pass

    def __apply_default_icon(self):
        logger.debug(f"窗口 {self.winfo_name()} 默认图标为 icon-48.png")
        self.iconphoto(True, PhotoImage(master=self, data=resources.read_binary("images/icon-48.png")))

    def __apply_default_events(self):
        self.protocol("WM_DELETE_WINDOW", lambda: self.event_generate(EVENT_EXIT))
        self.bind(EVENT_EXIT, lambda _: self.destroy())


class ExtendedTk(Tk, AppWindowExtension, ABC):
    _theme_applied: bool = False

    def __init__(self, **kw):
        super().__init__(**kw)
        with withdraw_cm(self):
            if not self._theme_applied:
                self.set_theme(create_platform_theme())
            AppWindowExtension.__init__(self)
            self.center()

    def set_theme(self, theme: Theme):
        theme.apply_theme(self, Style(self))
        self._theme_applied = True


class ExtendedToplevel(Toplevel, AppWindowExtension, ABC):
    def __init__(self, master: Tk | Toplevel, **kw):
        super().__init__(master, **kw)
        with withdraw_cm(self):
            AppWindowExtension.__init__(self)
            if isinstance(self.master, Tk) or isinstance(self.master, Toplevel):
                self.center(self.master)


class ExtendedDialog(Toplevel, AppWindowExtension, ABC):
    def __init__(self, master: Tk | Toplevel, **kw):
        super().__init__(master, **kw)
        with withdraw_cm(self):
            AppWindowExtension.__init__(self)
            if isinstance(self.master, Tk) or isinstance(self.master, Toplevel):
                self.center(self.master)

    @abstractmethod
    @override
    def on_init_window(self):
        self.bind("<Escape>", lambda _: self.event_generate(EVENT_EXIT))

        if isinstance(self.master, Wm):
            self.transient(self.master)
            self.resizable(False, False)
