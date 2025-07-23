from ctypes import WinError, get_last_error, windll
from typing import override

from vcf_generator_lite.utils.display.windows_2000_impl import Windows2000Display


class WindowsVistaDisplay(Windows2000Display):
    @override
    @staticmethod
    def enable_dpi_aware():
        result = bool(windll.user32.SetProcessDPIAware())
        if not result:
            raise WinError(get_last_error())
