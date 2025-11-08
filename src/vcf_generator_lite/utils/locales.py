import locale
import logging
import os
import tomllib
from importlib.resources.abc import Traversable
from typing import Any

from vcf_generator_lite.utils import resources

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, current_locale: str | None = None, fallback_locale: str = "zh_CN"):
        if current_locale is None:
            # 不要使用 locale.getlocale() 因为 https://github.com/python/cpython/issues/130796
            current_locale = locale.getdefaultlocale()[0]
        self.current_locale = current_locale
        self.fallback_locale = fallback_locale
        self.translations: dict[str, Any] = {}
        self.load_locales()

    def load_locale(self, locale_name: str, traversable: Traversable | None = None):
        if traversable is None:
            traversable = resources.traversable.joinpath("locales", f"{locale_name}.toml")
        with traversable.open("rb") as f:
            self.translations[locale_name] = tomllib.load(f)

    def load_locales(self):
        fallbacks: list[str | None] = [
            *(self.current_locale.split("_") if (self.current_locale is not None) else []),
            self.fallback_locale,
        ]
        for locale_traversable in resources.traversable.joinpath("locales").iterdir():
            locale_name = os.path.splitext(locale_traversable.name)[0]
            if locale_name in fallbacks:
                self.load_locale(locale_name, locale_traversable)

    def translate(self, key: str) -> str:
        fallbacks: list[str | None] = [
            *(self.current_locale.split("_") if (self.current_locale is not None) else []),
            self.fallback_locale,
        ]
        split_keys: list[str] = key.split(".")
        for fallback in fallbacks:
            if fallback is None or fallback not in self.translations:
                continue

            branch = self.translations[fallback]
            for split_key in split_keys:
                if split_key in branch:
                    branch = branch[split_key]
            if isinstance(branch, str):
                return branch

        raise KeyError(f"Key {key} not found in translations")

    def branch(self, branch: str):
        def branch_translate(key: str) -> str:
            return self.translate(f"{branch}.{key}")

        return branch_translate


translator = Translator()
t = translator.translate
branch = translator.branch
