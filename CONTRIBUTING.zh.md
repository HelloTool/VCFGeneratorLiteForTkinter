# 贡献指南

1. 在 [Gitee][RepositoryOnGitee] 或 [GitHub][RepositoryOnGithub] 平台中 Fork 本项目；
2. 使用 [Git](https://git-scm.com/) 克隆项目到本地：`git clone https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter.git`；
3. 创建分支，如 `feature/xxx` 或 `bugfix/xxx`；
4. 编写并提交代码；
5. 向本项目提交 Pull Request。

此外，有一些规范规则，请遵守：

## 图标生成

1. 图标使用 Fluent 设计
2. 生成大小为 `512x512` 的图标，重命名为 `icon.png`，放入 [`项目/docs/images`](./docs/images) 中；
3. 生成 `.ico` 图标与 48x48 的 `.png` 图标，分别命名为 `icon.ico` 与 `icon-48.png`，放入 [`项目/src/vcf_generator_lite/assets/images`](./src/vcf_generator_lite/assets/images) 中。

## 代码规范

- Python（`.py`）：[PEP8](https://www.python.org/dev/peps/pep-0008/)；
- Markdown（`.md`）：[Markdownlint](https://github.com/DavidAnson/markdownlint)。
  - 本项目未完全遵守 Markdownlint 规范，详情请参考 [.markdownlint.json](./.markdownlint.json)。

详情请参考 [.editorconfig](./.editorconfig)。

## GIT 提交规范

参考 Angular 的 [Commit Message Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format)。

## UI 设计

使用平台样式，并且建议遵循微软[《桌面应用程序的设计基础知识》](https://learn.microsoft.com/zh-cn/windows/win32/uxguide/designprinciples)。

注意事项：

- 代码中布局尺寸单位是点（`p`），而不是像素（`px`） 、[有效像素（`epx`）](https://learn.microsoft.com/zh-cn/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design#effective-pixels-and-scale-factor)；
- 本软件的点（`p`）单位与 Tkinter 默认的点（`p`）单位不同，本软件的点（`p`）的作用与有效像素（`epx`）的作用相同；
- 由于字体单位也使用点（`p`），因此在本软件中，字体的单位与有效像素（`epx`）相同，默认的字体大小为 `12p` 而非 `9p`。

[RepositoryOnGitee]: https://gitee.com/HelloTool/VCFGeneratorLiteForTkinter/
[RepositoryOnGithub]: https://github.com/HelloTool/VCFGeneratorLiteForTkinter/
