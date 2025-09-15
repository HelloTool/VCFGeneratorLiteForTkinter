from abc import ABC, abstractmethod


class DpiAware(ABC):
    @staticmethod
    @abstractmethod
    def enable_dpi_aware() -> bool: ...
