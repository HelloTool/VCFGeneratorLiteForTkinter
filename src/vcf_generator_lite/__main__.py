import logging
import os
import sys

from vcf_generator_lite import constants
from vcf_generator_lite.utils.dpi_aware import enable_dpi_aware
from vcf_generator_lite.utils.locales import branch
from vcf_generator_lite.windows.main import create_main_window

startup_t = branch("startup")


def fix_home_env():
    """
    修复 Tkinter 在 Windows 中无法获取 HOME 的问题
    """
    os.environ["HOME"] = os.path.expanduser("~")


def setup_logging():
    log_level = logging.DEBUG if __debug__ else logging.INFO
    logging.basicConfig(level=log_level, stream=sys.stdout)


def main():
    setup_logging()
    fix_home_env()
    enable_dpi_aware()

    logging.info(startup_t("starting"))
    print(startup_t("source_tip").format(url=constants.URL_REPOSITORY))

    main_window, _ = create_main_window()

    main_window.mainloop()

    logging.info(startup_t("exiting"))


if __name__ == "__main__":
    main()
