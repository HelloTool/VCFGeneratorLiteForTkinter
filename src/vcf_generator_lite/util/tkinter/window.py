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


def center_window(window: WindowOrExtension, parent: WindowOrExtension = None):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    vroot_width = window.winfo_vrootwidth()
    vroot_height = window.winfo_vrootheight()
    vroot_x = window.winfo_vrootx()
    vroot_y = window.winfo_vrooty()
    window_max_x = vroot_x + vroot_width - window_width
    window_max_y = vroot_y + vroot_height - window_height
    if parent is not None:
        # 使用winfo_x而不使用winfo_rootx在Windows上有更好的效果，winfo_x是包括边框的位置。
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent_x + (parent_width - window_width) // 2
        y = parent_y + (parent_height - window_height) // 2
    else:
        # maxsize不会包含任务栏高度，但是maxsize的值也会算上副屏，所以为了防止窗口超出当前屏幕，这里取最小值
        parent_maxsize = window.maxsize()
        parent_width = min(parent_maxsize[0], vroot_width)
        parent_height = min(parent_maxsize[1], vroot_height)
        x = (parent_width - window_width) // 2
        y = (parent_height - window_height) // 2
    x = max(min(x, window_max_x), vroot_x)
    y = max(min(y, window_max_y), vroot_y)
    window.geometry(f"+{x}+{y}")


class CenterWindowExtension(WindowExtension, ABC):

    def center(self, parent: WindowOrExtension = None):
        center_window(self, parent)


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
