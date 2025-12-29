from tkinter import Event

from vcf_generator_lite.core.vcf_generator import InvalidLine
from vcf_generator_lite.windows.invalid_lines.common import st
from vcf_generator_lite.windows.invalid_lines.window import InvalidLinesWindow


class InvalidLinesController:
    def __init__(
        self,
        window: InvalidLinesWindow,
        display_path: str,
        invalid_lines: list[InvalidLine],
    ):
        self.window = window
        window.bind("<Return>", self.on_ok_click)
        window.header_label.configure(text=st("message").format(path=display_path))
        for item in invalid_lines:
            window.content_tree.insert(
                parent="",
                index="end",
                id=item.row_position,
                values=(
                    st("cell_row").format(row=item.row_position + 1),
                    item.content,
                    item.reason,
                ),
            )

    def on_ok_click(self, _: Event):
        self.window.ok_button.invoke()
