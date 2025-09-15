import logging
import re
from tkinter import Misc
from typing import Any, overload

logger = logging.getLogger(__name__)


class ScalingMiscExtension(Misc):
    _scale_factor: float = 1.0

    def __init__(self):
        self._scale_factor = self.scaling()
        if __debug__:
            logger.debug(
                f"init with scale_factor={self._scale_factor}, "
                f"system scale is {round(self._scale_factor * 0.75, 2)}."
            )

    @overload
    def scaling(self, factor: None = None) -> float: ...

    @overload
    def scaling(self, factor: float) -> None: ...

    def scaling(self, factor: float | None = None):
        """
        设置或获取GUI缩放比例因子

        当传入factor参数时，设置当前缩放比例并应用新的缩放因子到Tkinter窗口。
        不传入参数时返回当前缩放比例因子。

        与 tk scaling ?-displayof window? ?number? 相同。
        """
        if factor is not None:
            self._scale_factor = factor
        return self.tk.call("tk", "scaling", factor)

    @overload
    def get_scaled(self, value: int) -> int: ...

    @overload
    def get_scaled(self, value: float) -> float: ...

    def get_scaled(self, value: int | float):
        if isinstance(value, int):
            return int(self._scale_factor * value)
        else:
            return float(self._scale_factor * value)

    def parse_dimen(self, value: str | int | float) -> float:
        if isinstance(value, int | float):
            return value
        match = re.match(r"([0-9.]+)([a-z]*)", value)
        if not match:
            raise ValueError(f"{value} is not a valid dimension")
        value = float(match.group(1))
        unit = match.group(2)
        if unit == "p" or unit == "pt":
            return value * self._scale_factor
        else:
            return float(value)

    def scale_kw(self, **kwargs: int | float) -> dict[str, Any]:
        return {key: self.get_scaled(value) for key, value in kwargs.items()}

    @overload
    def scale_args(self, *args: int) -> tuple[int, ...]: ...

    @overload
    def scale_args(self, *args: float) -> tuple[float, ...]: ...

    def scale_args(self, *args: int | float) -> tuple[Any, ...]:
        return tuple(self.get_scaled(value) for value in args)
