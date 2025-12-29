import copy
from tkinter.ttk import Scrollbar, Style, Treeview

from vcf_generator_lite.utils.graphics import FPixelPadding, parse_padding
from vcf_generator_lite.utils.tkinter.misc import scaled


class ScrolledTreeview(Treeview):

    def __init__(self, master=None, vertical=True, **kw):
        super().__init__(master, **kw)
        self.vbar: Scrollbar | None = None
        self._insets: FPixelPadding = FPixelPadding()

        if vertical:
            self._create_vertical_scrollbar()

    def _create_vertical_scrollbar(self):
        if not self.vbar:
            self.vbar = Scrollbar(self, orient="vertical")
            self.vbar.pack(side="right", fill="y", pady="1.5p", padx="1.5p")
            self.configure(yscrollcommand=self.vbar.set)
            self.apply_insets(
                copy.replace(
                    self._insets,
                    right=self.vbar.winfo_reqwidth() + scaled(self, 1.5),
                )
            )
            self.vbar.configure(command=self.yview)

    def apply_insets(self, insets: FPixelPadding):
        previous_insets = self._insets
        padding = self._get_widget_padding()
        new_padding = padding - previous_insets + insets
        self.configure(padding=new_padding.to_tuple())

    def _get_widget_padding(self) -> FPixelPadding:
        style = self.cget("style") or "Treeview"
        padding = self.cget("padding") or Style(self).lookup(style, "padding") or (0,)
        return parse_padding(self, padding)
