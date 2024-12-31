import logging

from vcf_generator import constants
from vcf_generator.ui.main import create_main_window
from vcf_generator.util import display


def main():
    logging.basicConfig(level=logging.INFO)
    display.set_process_dpi_aware()

    logging.info("Starting VCF Generator...")

    print(f"Tip: The source code is hosted at {constants.URL_SOURCE}")
    main_window, _ = create_main_window()
    main_window.mainloop()


if __name__ == "__main__":
    main()