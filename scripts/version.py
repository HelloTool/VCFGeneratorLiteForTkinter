import argparse
import re
import sys

import pyinstaller_versionfile


def get_exe_style_version(version: str):
    assert re.match(r"^(\d+\.)*\d+$", version), f"Invalid version: {version}"
    version_list: list[str] = version.split(".")
    while len(version_list) < 4:
        version_list.append("0")
    return ".".join(version_list[0:4])


def change_version(
    file_name: str, content_pattern: re.Pattern[str], content_formatter: str, version: str, encoding="utf-8"
):
    with open(file_name, "r", encoding=encoding) as f:
        origin_content = f.read()
    new_content = re.sub(content_pattern, content_formatter % version, origin_content)
    with open(file_name, "w", encoding=encoding) as f:
        f.write(new_content)
    print("Change version to %s in %s." % (version, file_name))


def change_pyproject_version(version: str):
    change_version(
        file_name="pyproject.toml",
        content_pattern=re.compile(r'^ *version *= *".*" *$', flags=re.M),
        content_formatter='version = "%s"',
        version=version,
    )


def change_version_info(version: str):
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file="vcf_generator_lite_versionfile.txt",
        input_file="vcf_generator_lite_metadata.yml",
        version=get_exe_style_version(version),
    )
    print("Change version to %s in %s." % (version, "vcf_generator_lite_versionfile.txt"))


def print_version():
    from vcf_generator_lite.__version__ import __version__

    print(__version__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", nargs="?", type=str)
    args = parser.parse_args()

    version = args.version
    if version:
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            print("Invalid version format. Version must be like '1.2.3'.", file=sys.stderr)
            return 1
        change_pyproject_version(version)
        change_version_info(version)
    else:
        print_version()
    return 0
