from abc import ABC, abstractmethod
from tkinter import Tk, Toplevel


class ThemePatch(ABC):
    @abstractmethod
    def configure_window(self, master: Tk | Toplevel):
        pass
