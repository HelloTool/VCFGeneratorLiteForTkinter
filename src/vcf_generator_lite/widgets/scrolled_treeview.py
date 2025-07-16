from tkinter.ttk import Treeview, Scrollbar, Style

from vcf_generator_lite.utils.tkinter.misc import ScalingMiscExtension


class ScrolledTreeview(Treeview, ScalingMiscExtension):

    def __init__(self, master=None, vertical=True, **kw):
        super().__init__(master, **kw)
        self.vbar: Scrollbar | None = None
        self._insets: tuple[int | float, int | float, int | float, int | float] = (0, 0, 0, 0)

        if vertical:
            self._create_vertical_scrollbar()

    def _create_vertical_scrollbar(self):
        if not self.vbar:
            self.vbar = Scrollbar(self, orient="vertical")
            self.vbar.pack(side="right", fill="y", pady="1.5p", padx="1.5p")
            self.configure(yscrollcommand=self.vbar.set)
            self.apply_insets(right=self.vbar.winfo_reqwidth() + self.get_scaled(1.5))
            self.vbar.configure(command=self.yview)

    def apply_insets(
        self,
        *,
        left: int | float | None = None,
        top: int | float | None = None,
        right: int | float | None = None,
        bottom: int | float | None = None,
    ):
        previous_insets = self._insets
        insets = self._insets = (left or 0, top or 0, right or 0, bottom or 0)
        padding = self._get_widget_padding()
        self.configure(
            padding=(
                padding[0] - previous_insets[0] + insets[0],
                padding[1] - previous_insets[1] + insets[1],
                padding[2] - previous_insets[2] + insets[2],
                padding[3] - previous_insets[3] + insets[3],
            )
        )

    def _get_widget_padding(self) -> tuple[float, float, float, float]:
        style = self.cget("style") or "Treeview"
        padding = self.cget("padding") or Style(self).lookup(style, "padding") or (0,)
        if isinstance(padding, str):
            padding = padding.split()
        left = self.parse_dimen(str(padding[0])) if len(padding) >= 1 else 0
        top = self.parse_dimen(str(padding[1])) if len(padding) >= 2 else left
        right = self.parse_dimen(str(padding[2])) if len(padding) >= 3 else left
        bottom = self.parse_dimen(str(padding[3])) if len(padding) >= 4 else top
        return left, top, right, bottom
