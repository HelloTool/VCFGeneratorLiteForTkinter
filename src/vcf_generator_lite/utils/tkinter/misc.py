import logging
from tkinter import Misc
from typing import Any, overload

logger = logging.getLogger(__name__)


@overload
def scaling(master: Misc, factor: None = None) -> float: ...
@overload
def scaling(master: Misc, factor: float) -> None: ...
def scaling(master: Misc, factor: float | None = None) -> float | None:
    """
    设置或获取 GUI 缩放比例因子

    当传入 factor 参数时，设置当前缩放比例并应用新的缩放因子到 Tkinter 窗口。
    不传入参数时返回当前缩放比例因子。

    与 tk scaling ?-displayof window? ?number? 相同。

    - Tk 手册页：https://www.tcl-lang.org/man/tcl8.6/TkCmd/tk.htm
    """
    if factor is not None:
        master.tk.call("tk", "scaling", factor)
        setattr(master.tk, "_scaling", factor)
    else:
        factor = getattr(master.tk, "_scaling")
        if factor is None:
            factor = master.tk.call("tk", "scaling")
            setattr(master.tk, "_scaling", factor)
        return factor


@overload
def scaled(master: Misc, value: int) -> int: ...
@overload
def scaled(master: Misc, value: float) -> float: ...
def scaled(master: Misc, value: int | float) -> int | float:
    if isinstance(value, int):
        return int(scaling(master) * value)
    else:
        return float(scaling(master) * value)


@overload
def scale_args(master: Misc, *args: int) -> tuple[int, ...]: ...
@overload
def scale_args(master: Misc, *args: float) -> tuple[float, ...]: ...
def scale_args(master: Misc, *args: int | float) -> tuple[Any, ...]:
    return tuple(scaled(master, value) for value in args)


def scale_kw(self, **kwargs: int | float) -> dict[str, Any]:
    return {key: self.get_scaled(value) for key, value in kwargs.items()}
