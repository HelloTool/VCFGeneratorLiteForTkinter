# 在旧版本 Windows 中运行

> [!WARNING] 免责声明
>
> **请注意，我们强烈不推荐普通用户进行以下操作，并在此明确相关风险：**
>
> - **无官方支持**：此方法非官方提供，应用开发团队**无法**为通过此方式安装的运行环境提供任何技术支持。后续使用中出现任何问题，请自行解决。
> - **安全风险**：第三方补丁可能包含恶意代码、病毒或后门。您必须从**可信的来源**获取补丁，并在安装前使用杀毒软件进行扫描。我们对因使用第三方补丁而导致的任何安全漏洞或数据丢失**不承担责任**。
> - **稳定性风险**：打补丁后的 Python 环境可能存在无法预料的崩溃、性能问题或兼容性错误，本应用在此环境下的行为**未经过测试，不保证稳定运行**。
> - **系统风险**：替换系统关键文件操作不当可能导致 Python 环境甚至部分系统功能损坏，需要重新安装 Python 或系统才能恢复。
>
> 选择使用第三方补丁意味着您已充分了解并自愿接受上述所有风险。本项目的开发者、贡献者及关联方​​对您使用第三方补丁可能造成的任何直接或间接损失（包括但不限于数据丢失、系统损坏、安全事件）概不负责​​。

## 方案一：使用 [PythonWin7][pythonwin7_repository_github] ![Windows 7、Windows 8](https://img.shields.io/badge/Windows_7、Windows_8-0078D4)

对于安装包、便携包，您需要使用 PythonWin7 内的文件替换本应用的文件：

1. **获取 Python 嵌入包**：从 [PythonWin7][pythonwin7_repository_github] 仓库下载：
   - `python-3.13.x-embed-amd64.zip`
2. **提取 DLL 文件**：解压下载的 ZIP 包，从中获取以下文件：
   - `python313.dll`  
   - `api-ms-win-core-path-l1-1-0.dll`
3. **修补程序**：
   1. 对于安装包，完成软件安装\
      对于便携包，解压该文件
   2. 打开安装目录下的 `_internal` 文件夹
   3. 将下载的两个 DLL 文件覆盖到该目录

对于 Python ZIP 应用，您只需要安装 PythonWin7 的 Python：

1. **获取 Python 安装包**：从 [PythonWin7][pythonwin7_repository_github] 仓库下载：
   - 64 位系统：`python-3.13.x-amd64-full.exe`
   - 32 位系统：`python-3.13.x-full.exe`
2. **安装 Python**：运行安装程序，按照提示进行安装。

## 方案二：使用 VxKex NEXT ![Windows 7](https://img.shields.io/badge/Windows_7-0078D4)

1. **安装 VxKex NEXT**：从 [VxKex NEXT][vxkex-next_release_github] 获取 Release 版本，按照提示进行安装。
2. **启用 VxKex NEXT**：打开 `C:\Program Files\VxKex NEXT\VxKex.exe`，选择 `Enable VxKex`，然后选择 `vcf_generator_lite.exe`。

对于安装包、便携包，您只需要为本应用目录中的 `vcf_generator_lite.exe` 启用 VxKex NEXT；
对于 Python ZIP 应用，由于 VxKex NEXT 的 bug，您无法为 Python 启动器启用，因此您无法直接运行 Python ZIP 应用。

<!-- ## 方案三：使用 One-Core-API ![Windows XP](https://img.shields.io/badge/Windows_Server_2003、Windows_XP-0078D4)

该方法适用于 Windows Server 2003 RTM、SP1 和 SP2、Windows XP RTM、SP1、SP2 和 SP3 以及 Windows XP x64 SP1/SP2。 -->

[pythonwin7_repository_github]: https://github.com/adang1345/PythonWin7
[vxkex-next_release_github]: https://github.com/YuZhouRen86/VxKex-NEXT/releases/latest
