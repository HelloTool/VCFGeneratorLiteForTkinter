<div align="center">
<img src="./docs/images/icon.svg" width="192" height="192" alt="App icon" />

# VCF 生成器 Lite

**仓库**：
[![Gitee 仓库](https://img.shields.io/badge/Gitee-仓库-C71D23?logo=gitee)][RepositoryOnGitee]
[![GitHub 仓库](https://img.shields.io/badge/GitHub-仓库-0969da?logo=github)][RepositoryOnGithub]

**平台**：
[![Windows7+ (exe)](https://img.shields.io/badge/Windows_7+-exe-0078D4?logo=windows)][ReleaseOnGitee]
[![Python3.12+ (pyzw)](https://img.shields.io/badge/Python_3.12+-pyzw-3776AB?logo=python&logoColor=f5f5f5)][ReleaseOnGitee]

**语言**：
**中文** |
[English](./README.md) |
<small>期待您的翻译！</small>

</div>

VCF 生成器，输入姓名与手机号则自动生成用于批量导入到通讯录内的 VCF 文件。

[![许可证](https://img.shields.io/github/license/HelloTool/VCFGeneratorLiteForTkinter?label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](./LICENSE)
[![贡献者公约](https://img.shields.io/badge/贡献者公约-2.1-4baaaa.svg)](./docs/CODE_OF_CONDUCT.zh.md)
[![代码风格：black](https://img.shields.io/badge/代码风格-black-000000.svg)](https://github.com/psf/black)

[![Test](https://github.com/HelloTool/VCFGeneratorLiteForTkinter/actions/workflows/test.yml/badge.svg)](https://github.com/HelloTool/VCFGeneratorLiteForTkinter/actions/workflows/test.yml)

## 软件截图

<img src="./docs/images/screenshots/main_window.webp" width="600" alt="主窗口" />

## 获取应用

### 获取软件包

您可以通过以下渠道获取软件包：

- [Gitee 发行版][ReleaseOnGitee]
- [GitHub Releases][ReleaseOnGithub]

不同系统的用户需要下载不同的文件，您可以根据下表进行选择：

| 操作系统 | Inno Setup 安装包     | 便携包（压缩文件） | Python ZIP 应用         |
| -------- | --------------------- | ------------------ | ----------------------- |
| Windows  | `*_setup.exe`（推荐） | `*_portable.zip`   | `*_zipapp.pyzw`         |
| Linux    | 暂未提供              | 暂未提供           | `*_zipapp.pyzw`（推荐） |
| macOS    | 暂未提供              | 暂未提供           | `*_zipapp.pyzw`（推荐） |
| Android  | 不支持                | 不支持             | 不支持                  |

## 使用方法

1. 把名字和电话以每行 `姓名 电话号码 备注` 的格式复制到主界面编辑框内，其中备注可忽略。例如：
   ```text
   张三	13345367789	著名的法外狂徒
   李四	13445467890
   王五	13554678907
   赵六	13645436748
   ```
2. 点击“生成”，选择一个路径保存文件。
3. 将生成后的 VCF 文件复制到手机内，打开文件时选择使用“通讯录”，然后根据提示操作。
4. 等待导入完成。

> [!NOTE] 说明
>
> - 制表符会自动转换为空格处理，您可以同时使用制表符和空格分割。
> - 程序会自动去除输入框内多余的空格。
>
> 例如 `东坡居士 苏轼   13333333333  眉州眉山人` 将会被识别为
>
> > - 姓名：东坡居士 苏轼
> > - 电话：13333333333
> > - 备注：眉州眉山人
>

## 兼容性

### 应用兼容性

应用支持 Windows 8.1 或更高版本。如果您想在 Windows 8 及以下版本中使用本应用，请参考[《在旧版本 Windows 中运行》](./docs/compatibility/runs-on-older_windows.md)。

| 系统环境              | 特性     | 详情                                    |
| --------------------- | -------- | --------------------------------------- |
| Windows 10 或更高版本 | 深色模式 | 不支持深色模式                          |
| Windows 10 或更高版本 | 显示缩放 | 切换 DPI 时，由操作系统自动完成缩放适配 |

### vCard 文件兼容性

本 APP 仅支持生成仅包含姓名和电话的 2.1 版本 vCard 文件。

| 第三方应用     | 详情                              |
| -------------- | --------------------------------- |
| Windows 联系人 | 非 UTF-8 环境下中文姓名会显示乱码 |

## 开发与贡献

请参阅[《开发指南》](./docs/dev/README.md)与[《贡献指南》](./docs/CONTRIBUTING.md)。

## 许可证

本项目以 Apache 2.0 许可证发布，详情请参阅 [LICENSE](./LICENSE)。

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

## 开源声明

请参见 [《开源声明》](./docs/legal/os_notices.md)

## 特别感谢

本项目部分代码由 DeepSeek、通义灵码 生成

[RepositoryOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/
[RepositoryOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/
[ReleaseOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
[ReleaseOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/releases/latest
