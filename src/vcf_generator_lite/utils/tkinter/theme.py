from abc import ABC, abstractmethod
from tkinter import Tk, Toplevel
from tkinter.ttk import Style


class EnhancedTheme(ABC):
    @abstractmethod
    def configure_tk(self, master: Tk, style: Style):
        pass

    @abstractmethod
    def configure_window(self, master: Tk | Toplevel, style: Style):
        pass
