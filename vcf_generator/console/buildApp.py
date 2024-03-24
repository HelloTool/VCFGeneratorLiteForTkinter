import argparse
import os

from vcf_generator.console.utils import get_bits
from vcf_generator.util import logger


def nuitka():
    """
    nuitka 在 UI 上有一些 BUG
    """
    os.system("nuitka main.py")


def pyinstaller():
    os.system("pyinstaller vcf_generator.spec --noconfirm")


def main():
    if get_bits() != 64:
        logger.error(f"Only 64 bit python is supported. Current version is {get_bits()}")
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-builder", "--builder", type=str, default="pyinstaller")
    args = parser.parse_args()

    builder = args.builder
    if builder not in ["nuitka", "pyinstaller"]:
        logger.error(f"Unknown builder: {builder}")
        return
    if builder == "nuitka":
        nuitka()
    elif builder == "pyinstaller":
        pyinstaller()