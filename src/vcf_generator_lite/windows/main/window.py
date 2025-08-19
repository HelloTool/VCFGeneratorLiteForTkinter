import urllib.parse
from tkinter import Misc
from tkinter.ttk import Button, Frame, Label, Progressbar, Sizegrip
from typing import override

from ttk_text.scrolled_text import ScrolledText

from vcf_generator_lite.constants import (
    EMAIL_JESSE205,
    URL_LICENSE,
    URL_OS_NOTICES,
    URL_RELEASES,
    URL_REPORT,
    URL_REPOSITORY,
)
from vcf_generator_lite.layouts.vertical_dialog_layout import VerticalDialogLayout
from vcf_generator_lite.utils.external_app import open_url_with_fallback
from vcf_generator_lite.utils.locales import branch, t
from vcf_generator_lite.utils.tkinter.menu import MenuBarWindowExtension, MenuCascade, MenuCommand, MenuSeparator
from vcf_generator_lite.utils.tkinter.widget import auto_wrap_configure_event
from vcf_generator_lite.widgets.menu import TextContextMenu
from vcf_generator_lite.windows.base import ExtendedTk
from vcf_generator_lite.windows.base.constants import EVENT_EXIT
from vcf_generator_lite.windows.main.constants import EVENT_ABOUT, EVENT_CLEAN_QUOTES, EVENT_GENERATE

window_t = branch("main_window")


class MainWindow(ExtendedTk, VerticalDialogLayout, MenuBarWindowExtension):
    generate_button: Button
    content_text: ScrolledText
    progress_bar: Progressbar

    def __init__(self):
        super().__init__(className="VCFGeneratorLite")

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.title(t("app_name"))
        self.wm_minsize_pt(300, 300)
        self.wm_size_pt(450, 450)
        self._create_widgets(self)
        self._create_menus()

    @override
    def _configure_ui(self):
        super()._configure_ui()
        self.content_text.focus_set()

    @override
    def _create_header(self, parent: Misc):
        description_label = Label(parent, text=window_t("usage"), justify="left")
        description_label.bind("<Configure>", auto_wrap_configure_event, "+")
        description_label.pack(fill="x", padx="7p", pady="7p")
        return description_label

    @override
    def _create_content(self, parent: Misc):
        content_frame = Frame(parent)
        self.content_text = ScrolledText(content_frame, undo=True, tabs="2c", tabstyle="wordprocessor", maxundo=5)
        self.content_text.insert(0.0, window_t("input_example"))
        self.content_text.edit_reset()
        self.content_text.pack(fill="both", expand=True, padx="7p", pady=0)
        text_context_menu = TextContextMenu(self.content_text)
        text_context_menu.bind_to_widget()
        return content_frame

    @override
    def _create_actions(self, parent: Misc):
        action_frame = Frame(parent)
        sizegrip = Sizegrip(action_frame)
        sizegrip.place(relx=1, rely=1, anchor="se")

        self.progress_bar = Progressbar(action_frame, orient="horizontal", length=200)
        self.progress_label = Label(master=action_frame, text=window_t("label_generating"))

        self.generate_button = Button(
            action_frame,
            text=window_t("button_generate"),
            default="active",
            command=lambda: self.event_generate(EVENT_GENERATE),
        )
        self.generate_button.pack(side="right", padx="7p", pady="7p")
        return action_frame

    def _create_menus(self):
        self.load_menu_bar_items(
            MenuCascade(
                label=window_t("menu_file"),
                items=[
                    MenuCommand(
                        label=window_t("menu_file_generate"),
                        command=lambda: self.event_generate(EVENT_GENERATE),
                        accelerator="Ctrl + S",
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_file_exit"),
                        command=lambda: self.event_generate(EVENT_EXIT),
                        accelerator="Alt + F4",
                    ),
                ],
            ),
            MenuCascade(
                label=window_t("menu_edit"),
                items=[
                    MenuCommand(
                        label=window_t("menu_edit_undo"),
                        command=lambda: self.__generate_focus_event("<<Undo>>"),
                        accelerator="Ctrl + Z",
                    ),
                    MenuCommand(
                        label=window_t("menu_edit_redo"),
                        command=lambda: self.__generate_focus_event("<<Redo>>"),
                        accelerator="Ctrl + Y",
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_edit_cut"),
                        command=lambda: self.__generate_focus_event("<<Cut>>"),
                        accelerator="Ctrl + X",
                    ),
                    MenuCommand(
                        label=window_t("menu_edit_copy"),
                        command=lambda: self.__generate_focus_event("<<Copy>>"),
                        accelerator="Ctrl + C",
                    ),
                    MenuCommand(
                        label=window_t("menu_edit_paste"),
                        command=lambda: self.__generate_focus_event("<<Paste>>"),
                        accelerator="Ctrl + V",
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_edit_select_all"),
                        command=lambda: self.__generate_focus_event("<<SelectAll>>"),
                        accelerator="Ctrl + A",
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_edit_clean_quotes"),
                        command=lambda: self.event_generate(EVENT_CLEAN_QUOTES),
                    ),
                ],
            ),
            MenuCascade(
                label=window_t("menu_help"),
                items=[
                    MenuCommand(
                        label=window_t("menu_help_repository"),
                        command=lambda: open_url_with_fallback(self, URL_REPOSITORY),
                    ),
                    MenuCommand(
                        label=window_t("menu_help_release"),
                        command=lambda: open_url_with_fallback(self, URL_RELEASES),
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_help_feedback"),
                        command=lambda: open_url_with_fallback(self, URL_REPORT),
                    ),
                    MenuCommand(
                        label=window_t("menu_help_contact"),
                        command=lambda: open_url_with_fallback(
                            self, str(urllib.parse.urlunsplit(("mailto", None, EMAIL_JESSE205, None, None)))
                        ),
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_help_license"),
                        command=lambda: open_url_with_fallback(self, URL_LICENSE),
                    ),
                    MenuCommand(
                        label=window_t("menu_help_os_notices"),
                        command=lambda: open_url_with_fallback(self, URL_OS_NOTICES),
                    ),
                    MenuSeparator(),
                    MenuCommand(
                        label=window_t("menu_help_about"),
                        command=lambda: self.event_generate(EVENT_ABOUT),
                    ),
                ],
            ),
        )

    def __generate_focus_event(self, sequence: str):
        if widget := self.focus_get():
            widget.event_generate(sequence)

    def set_text_content(self, content: str):
        self.content_text.replace(1.0, "end", content)

    def get_text_content(self) -> str:
        return self.content_text.get(1.0, "end")[:-1]

    def show_progress(self):
        self.progress_bar.pack(side="left", padx="7p", pady="7p")
        self.progress_label.pack(side="left", padx=(0, "7p"), pady="7p")

    def hide_progress(self):
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()

    def set_progress(self, progress: float):
        self.progress_bar.configure(value=progress)

    def set_progress_determinate(self, value: bool):
        previous_value: bool = self.progress_bar.cget("mode") == "determinate"
        if previous_value != previous_value:
            return
        if value:
            self.progress_bar.configure(mode="determinate", maximum=1)
            self.progress_bar.stop()
        else:
            self.progress_bar.configure(mode="indeterminate", maximum=10)
            self.progress_bar.start()

    def set_generate_enabled(self, enabled: bool):
        self.generate_button.configure(state="normal" if enabled else "disabled")
