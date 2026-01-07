from tkinter import Tk

from vcf_generator_lite.themes.abs import ThemePatch
from vcf_generator_lite.utils.environment import is_windows

__all__ = ["create_theme_patch"]


def create_theme_patch(app: Tk, theme_name: str) -> ThemePatch:
    if is_windows and theme_name == "vista":
        from vcf_generator_lite.themes.vista_patch import VistaThemePatch

        return VistaThemePatch(app)

    from vcf_generator_lite.themes.default_patch import DefaultThemePatch

    return DefaultThemePatch(app)
