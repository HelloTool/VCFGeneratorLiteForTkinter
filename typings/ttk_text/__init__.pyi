"""
This type stub file was generated by pyright.
"""

from tkinter import Event, EventType, Grid, Pack, Place, Text
from tkinter.ttk import Frame, Style
from typing import Any, Dict
from ttk_text.utils import parse_padding

__all__ = ["ThemedText"]
_DYNAMIC_OPTIONS_TEXT = ...

class ThemedText(Text):
    """
    A themed text widget combining Tkinter Text with ttk Frame styling.

    This widget provides native Tkinter Text functionality with ttk theme support.
    Inherits from `tkinter.Text` while embedding a ttk.Frame for style management.

    Style Elements:
        - Style name: 'ThemedText.TEntry' (configurable via style parameter)
        - Theme states: [focus, hover, pressed] with automatic state transitions

    Default Events:
        <FocusIn>       - Activates focus styling
        <FocusOut>      - Deactivates focus styling
        <Enter>         - Applies hover state
        <Leave>         - Clears hover state
        <ButtonPress-1> - Sets pressed state (left mouse down)
        <ButtonRelease-1> - Clears pressed state (left mouse up)
        <<ThemeChanged>> - Handles theme reload events

    Geometry Management:
        Proxies all ttk.Frame geometry methods (pack/grid/place) while maintaining
        native Text widget functionality. Use standard geometry managers as with
        regular ttk widgets.

    Inheritance Chain:
        ThemedText → tkinter.Text → tkinter.Widget → tkinter.BaseWidget → object
    """

    def __init__(self, master=..., *, relief=..., style=..., class_=..., **kwargs) -> None:
        """Initialize a themed text widget.

        :param master: Parent widget (default=None)
        :param relief: Frame relief style (None for theme default)
        :param style: ttk style name (default='TextFrame.TEntry')
        :param class_: Widget class name (default='TextFrame')
        :param kw: Additional Text widget configuration options
        """
        ...

    def configure(self, cnf: Dict[str, Any] = ..., **kwargs):  # -> None:
        ...
    config = ...
    def __str__(self) -> str: ...

def example():  # -> None:
    ...

if __name__ == "__main__":
    ...
