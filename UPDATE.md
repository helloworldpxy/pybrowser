# PyBrowser 更新日志

## v2.5 (2026-06-17)

> 基于原 PyBrowser 进行全面重构，从单文件架构升级为模块化架构。

### 架构重构

#### 🏗️ 模块化拆分
- **单文件 → 模块化**：将原 ~700 行的 `browser.py` 拆分为 3 个模块目录、11 个源文件
- **core/** — 核心模块：`WebView` 自定义组件、`TabManager` 标签页管理器
- **ui/** — 用户界面：`NavigationToolbar`、`Sidebar`、`SettingsDialog`、`BookmarkManagerDialog`、`ThemeManager` 主题管理
- **utils/** — 工具模块：`HistoryManager`、`BookmarkManager`、`SettingsManager`

#### 🎨 UI 重构
- **样式集中管理**：所有样式表统一在 `ThemeManager` 中管理，消除内联 CSS 重复
- **暗色/亮色主题**：新增 `ThemeManager` 单例，支持明暗主题切换
- **组件解耦**：各 UI 组件通过信号槽通信，降低耦合度

#### 💾 数据持久化
- **历史记录持久化**：浏览历史自动保存到 `~/.pybrowser/history.json`
- **设置持久化**：浏览器设置保存到 `~/.pybrowser/settings.json`
- **书签优化**：书签保存到 `~/.pybrowser/bookmarks.json`，与项目目录解耦

#### ⌨️ 快捷键支持
- `Ctrl+T` — 新建标签页
- `Ctrl+W` — 关闭当前标签页
- `Ctrl+L` — 聚焦地址栏
- `F5` — 刷新页面
- `Ctrl+D` — 添加书签
- `Ctrl+Shift+T` — 切换明暗主题

#### 📦 其他改进
- **许可证变更**：从 GPL-3.0 更换为 PolyForm Noncommercial License 1.0.0
- **Conda 环境**：新增 `environment.yml`，支持 `conda env create` 一键构建环境
- **环境名称**：`pyb`
- **移除 icons 目录**：改用 Qt 内置 `QStyle` 图标，减小项目体积
- **错误处理**：改进异常处理和日志记录
- **类型提示**：核心模块添加类型提示（Type Hints）

### 已知限制
- 基于 PyQt5，Qt 5.15 LTS 已停止新功能开发
- 后续 UI 和功能更新将在 [NTPyBrowser](https://github.com/helloworldpxy/pybrowser)（PySide6 版本）上推出
