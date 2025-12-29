from tkinter import Label
from tkinter.ttk import Label as TtkLabel


def enable_auto_wrap(widget: Label | TtkLabel):
    widget.bind("<Configure>", lambda event: widget.configure(wraplength=event.width), "+")
