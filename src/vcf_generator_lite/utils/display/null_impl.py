from tkinter import Misc
from typing import override

from vcf_generator_lite.utils.display.base import Display


class NullDisplay(Display):
    @override
    @staticmethod
    def get_default_scale_factor(misc: Misc) -> float:
        return 1.0

    @override
    @staticmethod
    def enable_dpi_aware():
        pass
