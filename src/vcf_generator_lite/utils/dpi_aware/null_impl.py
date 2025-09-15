from typing import override

from vcf_generator_lite.utils.dpi_aware import DpiAware


class NullDpiAware(DpiAware):
    @override
    @staticmethod
    def enable_dpi_aware() -> bool:
        return False
