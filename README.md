<div align="center">
<img src="./docs/images/icon.svg" width="192" height="192" alt="App icon" />

# VCF Generator Lite

**Repositories**:
[![Gitee repository](https://img.shields.io/badge/Gitee-repository-C71D23?logo=gitee)][RepositoryOnGitee]
[![GitHub repository](https://img.shields.io/badge/GitHub-repository-0969da?logo=github)][RepositoryOnGithub]

**Platforms**:
[![Windows7+ (exe)](https://img.shields.io/badge/Windows_7+-exe-0078D4?logo=windows)][ReleaseOnGitee]
[![Python3.12+ (pyzw)](https://img.shields.io/badge/Python_3.12+-pyzw-3776AB?logo=python&logoColor=f5f5f5)][ReleaseOnGitee]

**Languages**:
[中文](./README.zh.md) |
**English** |
<small>More translations are welcome!</small>

</div>

VCF generator, input name and phone number to automatically generate VCF files for batch importing into the address book.

[![License](https://img.shields.io/github/license/HelloTool/VCFGeneratorLiteForTkinter)](./LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./docs/CODE_OF_CONDUCT.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Test](https://github.com/HelloTool/VCFGeneratorLiteForTkinter/actions/workflows/test.yml/badge.svg)](https://github.com/HelloTool/VCFGeneratorLiteForTkinter/actions/workflows/test.yml)

## Screenshot

<img src="./docs/images/screenshots/main_window.webp" width="600" alt="Main window" />

## Download

### Package Types

This application provides multiple package types, and you can make your selection according to the table below:

| Package Type     | Running Method                             | Applicable Scenarios                   |
| ---------------- | ------------------------------------------ | -------------------------------------- |
| Installer        | Install via setup program                  | Long-term use / Need desktop shortcuts |
| Portable Package | Extract and use (supports USB portability) | No installation / Temporary use        |
| Zip Application  | Double-click to run                        | Quick launch / Cross-platform use      |

| Package Type               | System Environment       | Notes                                                                  |
| -------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| Installer/Portable Package | Windows 7+ 64-bits       | Windows 7 requires patch files (See the "Compatibility" section below) |
| Zip Application            | Python 3.12+ and Tkinter | -                                                                      |

### Get the Packages

Get the software package through the following channels:

- [Gitee Releases][ReleaseOnGitee]
- [GitHub Releases][ReleaseOnGithub]

Users of different systems need to download different files. You can make your selection according to the table below:

| Package Type     | Windows                     | Linux                         | macOS                         | Android       |
| ---------------- | --------------------------- | ----------------------------- | ----------------------------- | ------------- |
| Installer        | `*_setup.exe` (recommended) | Not available                 | Not available                 | Not supported |
| Portable Package | `*_portable.zip`            | Not available                 | Not available                 | Not supported |
| Zip Application  | `*_zipapp.pyzw`             | `*_zipapp.pyzw` (recommended) | `*_zipapp.pyzw` (recommended) | Not supported |

## Usage

1. Open the app.
2. Copy the name and phone number in the format of `Name PhoneNumber Note` on each line into the editing box below. The note can be omitted.
   ```text
   Isaac Newton	13445467890	British mathematician
   Muhammad		13554678907
   Confucius		13645436748
   ```
3. Click "Generate", select a path to save the file.
4. Copy the generated VCF file to your phone, select "Contacts" when opening the file, and then follow the prompts.
5. Wait for the import to complete.

> [!NOTE] Note
>
> - Tabs will be automatically converted to spaces for processing.
> - The program will automatically remove extra spaces from the input box.
> - If there are multiple spaces in each line, all characters before the last space will be treated as names.
>
> For example, ` Han Meimei   13333333333   A   well-known girl` will be recognized as
>
>
> > - Name: Han Meimei
> > - Phone: 13333333333
> > - Note: A well-known girl
>

## Compatibility

### Application Compatibility

| System Environment | Feature         | Compatibility                                                                                  |
| ------------------ | --------------- | ---------------------------------------------------------------------------------------------- |
| Windows 10+        | Dark Mode       | Dark mode not supported                                                                        |
| Windows 10+        | Display Scaling | Unable to auto-scale when switching DPI; scaling adaptation is handled by the operating system |
| Windows 10+        | Font Scaling    | Font scaling not supported                                                                     |
| Windows 7+         | Display Scaling | Icon scaling only supports 100%, 125%, and 150% levels                                         |
| Windows 7 ~ 8.1    | App Launch      | Requires patches                                                                               |

#### Special Notes

<details>
<summary>Compatibility Patch Guide (Windows 7 ONLY)</summary>

1. **Download Python embed package** from [PythonWin7][PythonWin7RepositoryOnGithub]:
   - `python-3.13.2-embed-amd64.zip`
2. **Extract required DLLs**:
   - `python313.dll`
   - `api-ms-win-core-path-l1-1-0.dll`
3. **Apply patch**:
   1. Complete software installation
   2. Navigate to `_internal` folder in installation directory
   3. Replace existing files with the extracted DLLs

</details>

### vCard File Compatibility

This app only supports generating version 2.1 vCard files that contain only name and phone number.

| Third-party Application | Compatibility                                              |
| ----------------------- | ---------------------------------------------------------- |
| Windows Contacts        | Chinese names may appear garbled in non-UTF-8 environments |

## Development & Contribution

Please refer to the [Development Guide (Chinese)](./docs/dev/README.md) and the [Contribution Guide (Chinese)](./docs/CONTRIBUTING.md).

## License

This project is released under the Apache 2.0 license. For details, please refer to [LICENSE](./LICENSE).

```txt
Copyright 2023-2025 Jesse205

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Open Source Notice

Please refer to [Open Source Notice (Chinese)](./docs/legal/os_notices.md)

## Special Thanks

Part of the code in this project was generated by DeepSeek and Tongyi Lingma.

[RepositoryOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/
[RepositoryOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/
[ReleaseOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
[ReleaseOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
[PythonWin7RepositoryOnGithub]: https://github.com/adang1345/PythonWin7
