import gc
from abc import ABC
from contextlib import contextmanager
from tkinter import Misc, Tk, Toplevel, Wm, Event
from typing import Optional, Literal

from vcf_generator_lite.util.tkinter.misc import ScalingMiscExtension

type Window = Tk | Toplevel


class WindowExtension(Misc, Wm, ABC):
    pass


type WindowOrExtension = Window | WindowExtension


class GeometryWindowExtension(ScalingMiscExtension, WindowExtension, ABC):
    def wm_size(self, width: int, height: int):
        self.wm_geometry(f"{width}x{height}")

    def wm_size_pt(self, width: int, height: int):
        """
        设置窗口大小
        注：窗口大小单位为虚拟像素
        """
        self.wm_size(*self.scale_args(width, height))

    def wm_minsize_pt(self, width: int, height: int):
        return self.wm_minsize(*self.scale_args(width, height))

    def wm_maxsize_pt(self, width: int, height: int):
        return self.wm_maxsize(*self.scale_args(width, height))


class GcWindowExtension(WindowExtension, ABC):
    def __init__(self):
        super().__init__()
        self.bind("<Destroy>", self._on_destroy, "+")

    def _on_destroy(self, event: Event):
        if event.widget == self:
            gc.collect()


type WindowingSystem = Literal["x11", "win32", "aqua"]


class WindowingSystemWindowExtension(WindowExtension, ABC):
    _windowing_system_cached: Optional[WindowingSystem] = None

    @property
    def tk_windowing_system(self) -> WindowingSystem:
        if self._windowing_system_cached is not None:
            return self._windowing_system_cached
        ws = self._windowing_system_cached = self.tk.call('tk', 'windowingsystem')
        return ws


class CenterWindowExtension(WindowingSystemWindowExtension, WindowExtension, ABC):

    def center(self, reference_window: WindowOrExtension = None):
        if self.tk_windowing_system == "x11":
            self.deiconify()
        self.update()
        # 在拥有副屏的情况下，winfo_vrootwidth会比屏幕宽度长，所以应该与屏幕宽度取最小值
        screen_width = min(self.winfo_screenwidth(), self.winfo_vrootwidth())
        screen_height = min(self.winfo_screenheight(), self.winfo_vrootheight())
        if reference_window is not None:
            # 使用winfo_x而不使用winfo_rootx在Windows上有更好的效果，winfo_x是包括边框的位置。
            x = reference_window.winfo_x() + (reference_window.winfo_width() - self.winfo_width()) // 2
            y = reference_window.winfo_y() + (reference_window.winfo_height() - self.winfo_height()) // 2
        else:
            x = (screen_width - self.winfo_width()) // 2
            y = (screen_height - self.winfo_height()) // 2
        vroot_x = self.winfo_vrootx()
        vroot_y = self.winfo_vrooty()
        window_max_x = vroot_x + screen_width - self.winfo_width()
        window_max_y = vroot_y + screen_height - self.winfo_height()
        x = max(min(x, window_max_x), vroot_x)
        y = max(min(y, window_max_y), vroot_y)
        self.geometry(f"+{x}+{y}")

    def center_reference_master(self):
        self.center(self.master if isinstance(self.master, Tk | Toplevel) else None)


@contextmanager
def withdraw_cm(wm: Wm):
    """
    窗口隐藏上下文管理器

    专门解决 Tkinter 窗口初始化时因设置属性导致的闪烁问题。通过上下文管理器在初始化期间隐藏窗口，
    所有属性配置完成后再显示窗口，避免窗口在左上角短暂闪现的异常现象。
    """
    wm.wm_withdraw()
    yield
    wm.wm_deiconify()
