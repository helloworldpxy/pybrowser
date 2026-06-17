# PyBrowser 浏览器项目

![License](https://img.shields.io/badge/License-PolyForm%20Noncommercial%201.0.0-green)
![Version](https://img.shields.io/badge/Version-2.5-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

## 项目简介

基于 PyQt5 和 QtWebEngine 构建的轻量级网页浏览器，采用模块化架构设计，支持多标签页浏览和基础导航功能。

> ⚠️ **重要声明**  
> 本项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE) 许可证，**禁止商业用途**。  
> **禁止将本项目用于任何比赛、竞赛或学术评估目的。**  
> 如需将本项目用于比赛用途，请联系作者获取授权：[hklpl@icloud.com](mailto:hklpl@icloud.com)

> 📢 **维护说明**
> 在 v3.0 版本发布之前，PyBrowser 仅进行 **功能稳定性方面的维护**，所有 UI 和功能的更新均在 [NTPyBrowser](https://github.com/helloworldpxy/ntpybrowser)（基于 PySide6 的新架构版本）上推出。
> 追求 **稳定性的用户请选择 PyBrowser**，追求 **新功能和新 UI 的用户请选择 NTPyBrowser**。
> 预计在 v3.0 版本，NTPyBrowser 的改进将并入 PyBrowser 主线，届时 NTPyBrowser 项目将停止更新。

## 功能特性

- **模块化架构**  
  采用现代化的模块化设计，代码结构清晰，易于维护和扩展。

- **多标签页管理**  
  轻松打开、关闭和切换标签页。支持快捷键操作。

- **导航控制**  
  提供前进、后退、停止加载和刷新按钮，确保流畅的浏览体验。

- **智能地址栏**  
  自动补全 `http://`（若用户未输入协议头）。按回车键加载目标网页。

- **动态标签页标题**  
  标签页标题会随当前网页标题自动更新。

- **书签管理**  
  支持添加、删除和管理书签，数据自动持久化保存。

- **浏览历史记录**  
  自动记录浏览历史，支持查看和清除历史记录。

- **数据持久化**  
  书签、历史记录和设置自动保存到本地文件，重启后数据不丢失。

- **快捷键支持**  
  - `Ctrl+T`: 新建标签页
  - `Ctrl+W`: 关闭当前标签页
  - `Ctrl+L`: 聚焦地址栏
  - `F5`: 刷新页面
  - `Ctrl+D`: 添加书签
  - `Ctrl+Shift+T`: 切换明暗主题

- **明暗主题切换**  
  支持暗色和亮色两种主题，可通过工具栏按钮或快捷键 `Ctrl+Shift+T` 切换，主题偏好自动保存。

- **安全状态显示**  
  实时显示当前网页的安全状态（HTTPS/HTTP）。

## 项目结构

```
pybrowser/
├── main.py              # 主入口文件
├── core/                # 核心模块
│   ├── __init__.py
│   ├── web_view.py      # 自定义 WebView 组件
│   └── tab_manager.py   # 标签页管理器
├── ui/                  # 用户界面模块
│   ├── __init__.py
│   ├── toolbar.py       # 导航工具栏
│   ├── sidebar.py       # 侧边栏组件
│   ├── dialogs.py       # 对话框组件
│   └── styles.py        # 样式表集中管理
├── utils/               # 工具模块
│   ├── __init__.py
│   ├── history.py       # 历史记录管理
│   ├── bookmarks.py     # 书签管理
│   └── settings.py      # 设置管理
├── LICENSE              # 许可证文件
├── README.md            # 项目说明文档
└── environment.yml      # Conda 环境配置文件
```

## 安装指南

### 方式一：使用 Conda（推荐）

1. 克隆仓库：
   ```bash
   git clone https://github.com/helloworldpxy/pybrowser.git
   cd pybrowser
   ```

2. 创建并激活 Conda 环境：
   ```bash
   conda env create -f environment.yml
   conda activate pyb
   ```

3. 运行浏览器：
   ```bash
   python main.py
   ```

### 方式二：使用 pip

1. 克隆仓库：
   ```bash
   git clone https://github.com/helloworldpxy/pybrowser.git
   cd pybrowser
   ```

2. 安装依赖库：
   ```bash
   pip install PyQt5>=5.15.0 PyQtWebEngine>=5.15.0
   ```

3. 运行浏览器：
   ```bash
   python main.py
   ```

### 依赖环境

- Python 3.7 或更高版本
- PyQt5>=5.15.0
- PyQtWebEngine>=5.15.0

## 配置文件位置

PyBrowser 的配置文件保存在用户主目录下的 `.pybrowser` 文件夹中：

- **Windows**: `C:\Users\<用户名>\.pybrowser\`
- **macOS**: `/Users/<用户名>/.pybrowser/`
- **Linux**: `/home/<用户名>/.pybrowser/`

配置文件包括：
- `settings.json`: 浏览器设置
- `bookmarks.json`: 书签数据
- `history.json`: 历史记录

## 开发者

- **开发者**: [helloworldpxy](https://github.com/helloworldpxy)
- **GitHub**: https://github.com/helloworldpxy/pybrowser
- **版本**: 2.5
- **构建日期**: 2026-06-17

## 许可证

本项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE) 许可证。

**重要提示：**
- ✅ 允许：个人学习、研究、非商业用途
- ❌ 禁止：商业用途、比赛用途（未经授权）
- 📧 比赛用途授权请联系：[hklpl@icloud.com](mailto:hklpl@icloud.com)

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- **邮箱**: [hklpl@icloud.com](mailto:hklpl@icloud.com)
- **GitHub Issues**: https://github.com/helloworldpxy/pybrowser/issues

## 致谢

感谢所有为本项目做出贡献的开发者！

---

© 2026 helloworldpxy. All rights reserved.
