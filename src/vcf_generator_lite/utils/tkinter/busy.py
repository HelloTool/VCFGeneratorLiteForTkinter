from tkinter import Misc


def tk_buy_hold(master: Misc):
    if hasattr(master, "tk_buy_hold"):
        # noinspection PyUnresolvedReferences
        master.tk_busy_hold()  # pyright: ignore[reportAttributeAccessIssue, reportCallIssue]
    else:
        master.tk.call("tk", "busy", "hold", str(master))


def tk_busy_forget(master: Misc):
    if hasattr(master, "tk_busy_forget"):
        # noinspection PyUnresolvedReferences
        master.tk_busy_forget()  # pyright: ignore[reportAttributeAccessIssue]
    else:
        master.tk.call("tk", "busy", "forget", str(master))
