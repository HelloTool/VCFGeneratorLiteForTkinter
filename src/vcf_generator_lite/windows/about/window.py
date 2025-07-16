from tkinter import Label as TkLabel
from tkinter import Misc, PhotoImage
from tkinter.ttk import Button, Frame, Label, Style
from typing import override

from vcf_generator_lite import constants
from vcf_generator_lite.__version__ import __version__
from vcf_generator_lite.constants import APP_COPYRIGHT
from vcf_generator_lite.layouts.vertical_dialog_layout import VerticalDialogLayout
from vcf_generator_lite.utils import resources
from vcf_generator_lite.utils.locales import branch, t
from vcf_generator_lite.utils.tkinter.font import extend_font_scale
from vcf_generator_lite.widgets.menu import TextContextMenu
from vcf_generator_lite.widgets.tkhtmlview import HTMLScrolledText
from vcf_generator_lite.windows.base import ExtendedDialog
from vcf_generator_lite.windows.base.constants import EVENT_EXIT

window_t = branch("about_window")


class AboutWindow(ExtendedDialog, VerticalDialogLayout):
    app_icon_image: PhotoImage

    @override
    def _configure_ui_withdraw(self):
        super()._configure_ui_withdraw()
        self.title(window_t("title"))
        self.wm_size_pt(375, 300)
        self.wm_minsize_pt(375, 300)
        self.wm_maxsize_pt(375, 300)
        self._create_widgets(self)

    @override
    def _create_header(self, parent: Misc):
        header_frame = Frame(parent, style="DialogHeader.TFrame")
        background_color = Style(parent).lookup("DialogHeader.TFrame", "background")
        # 保存到 Window 中防止回收内存
        self.app_icon_image = PhotoImage(
            master=self,
            data=resources.read_scaled_binary(
                resources={
                    1.0: "images/icon-48.png",
                    1.25: "images/icon-60.png",
                    1.5: "images/icon-72.png",
                },
                scaling=round(self.scaling() * 0.75, 2),
            ),
        )
        app_icon_label = TkLabel(
            header_frame,
            image=self.app_icon_image,
            background=background_color,
            width="36p",
            height="36p",
        )
        app_icon_label.pack(side="left", padx="14p", pady="7p")

        app_info_frame = Frame(header_frame, style="DialogHeaderContent.TFrame")
        app_info_frame.pack(side="left", anchor="center", fill="x", expand=True, padx=(0, "14p"), pady="14p")

        app_name_label = Label(
            app_info_frame,
            text=window_t("label_app_name").format(version=__version__),
            style="DialogHeaderContent.TLabel",
            font=extend_font_scale("TkDefaultFont", 12 / 9),
        )
        app_name_label.pack(anchor="w")
        app_copyright_label = Label(app_info_frame, text=APP_COPYRIGHT, style="DialogHeaderContent.TLabel")
        app_copyright_label.pack(anchor="w")
        return header_frame

    @override
    def _create_content(self, parent: Misc):
        content_frame = Frame(parent)
        details_input = HTMLScrolledText(
            content_frame,
            html=resources.read_text("texts/about.html").format(
                heading_links=window_t("heading_links"),
                label_repository=window_t("label_repository"),
                repository_url=constants.URL_REPOSITORY,
                label_release=window_t("label_release"),
                release_url=constants.URL_RELEASES,
                heading_contact=window_t("heading_contact"),
                label_email=window_t("label_email"),
                jesse205_email=constants.EMAIL_JESSE205,
                heading_legal=window_t("heading_legal"),
                label_os_notices=window_t("label_os_notices"),
                os_notices_url=constants.URL_OS_NOTICES,
            ),
            state="disabled",
        )
        details_input.pack(fill="both", expand=True, padx="7p", pady=("7p", 0))
        details_context_menu = TextContextMenu(details_input)
        details_context_menu.bind_to_widget()
        return content_frame

    @override
    def _create_actions(self, parent: Misc):
        action_frame = Frame(parent)
        self.ok_button = Button(
            action_frame, text=t("button_ok"), default="active", command=lambda: self.event_generate(EVENT_EXIT)
        )
        self.ok_button.pack(side="right", padx="7p", pady="7p")
        return action_frame
