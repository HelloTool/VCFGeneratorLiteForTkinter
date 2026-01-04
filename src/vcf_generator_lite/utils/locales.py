import locale
import logging
import os
import tomllib
from importlib.resources.abc import Traversable
from typing import Any

from vcf_generator_lite.utils import resources

logger = logging.getLogger(__name__)


def get_fallback_traversable_list(locale_name: str) -> list[Traversable]:
    locale_name_parts = locale_name.split("_")
    fallback_names = [locale_name_parts[0]]
    for part in locale_name_parts[1:]:
        fallback_names.extend([f"{head_name}_{part}" for head_name in fallback_names])

    fallback_traversable_list: list[Traversable] = []
    for traversable in resources.traversable.joinpath("locales").iterdir():
        traversable_name = os.path.splitext(traversable.name)[0]
        if traversable_name in fallback_names:
            fallback_traversable_list.append(traversable)
            if len(fallback_traversable_list) == len(fallback_names):
                break
    fallback_traversable_list.reverse()
    return fallback_traversable_list


def deep_get(obj: dict[str, Any] | str, split_keys: list[str]) -> Any:
    branch: dict[str, Any] | str = obj
    for split_key in split_keys:
        if not isinstance(branch, dict):
            return None
        if split_key in branch:
            branch = branch[split_key]
    else:
        return branch


class Translator:
    def __init__(self, current_locale: str | None = None, fallback_locale: str = "en"):
        if current_locale is None:
            # 不要使用 locale.getlocale() 因为 https://github.com/python/cpython/issues/130796
            current_locale = locale.getdefaultlocale()[0]
        self.loaded_translations: list[dict[str, Any]] = []
        current_traversable_list = get_fallback_traversable_list(current_locale) if current_locale is not None else []
        self.fallback_traversable_list = [
            *current_traversable_list,
            *get_fallback_traversable_list(fallback_locale),
        ]

    def translate(self, key: str) -> str:
        split_keys: list[str] = key.split(".")
        for translations in self.loaded_translations:
            result = deep_get(translations, split_keys)
            if isinstance(result, str):
                return result
        while self.fallback_traversable_list:
            translations = self.load_translation()
            result = deep_get(translations, split_keys)
            if isinstance(result, str):
                return result

        raise KeyError(f"Key {key} not found in translations")

    def load_translation(self):
        traversable = self.fallback_traversable_list.pop(0)
        with traversable.open("rb") as f:
            result = tomllib.load(f)
            self.loaded_translations.append(result)
        return result

    def scope(self, scope: str):
        def branch_translate(key: str) -> str:
            return self.translate(f"{scope}.{key}")

        return branch_translate


translator = Translator()
t = translator.translate
scope = translator.scope
