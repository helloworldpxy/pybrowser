# Pybrowser浏览器项目

![License](https://img.shields.io/badge/License-GPL--3.0-green)

## 项目简介
基于 PyQt5 和 QtWebEngine 构建的轻量级网页浏览器，支持多标签页浏览和基础导航功能。

## 功能特性

- **多标签页管理**  
  轻松打开、关闭和切换标签页。双击标签栏可新建标签页。

- **导航控制**  
  提供前进、后退、停止加载和刷新按钮，确保流畅的浏览体验。

- **智能地址栏**  
  自动补全 `http://`（若用户未输入协议头）。按回车键加载目标网页。

- **动态标签页标题**  
  标签页标题会随当前网页标题自动更新。

- **简洁交互界面**  
  直观的图标按钮和响应式布局，操作一目了然。

## 安装指南

### 依赖环境
- Python 3.7 或更高版本
- PyQt5>=5.15.0
- PyQtWebEngine>=5.15.0

### 安装步骤
1. 克隆仓库：
   ```bash
   git clone https://github.com/helloworldpxy/pybrowser.git
   cd pybrowser
   ```

2. 安装依赖库：
   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

3. 确保 `icons` 目录包含所需图标文件（如 `back.png`, `forward.png` 等）。（v2.0版本不需要icons目录）

4. 运行浏览器：
   ```bash
   python browser.py
   ```

## 使用说明

- **新建标签页**：点击导航栏的 "+" 按钮（若已实现）或双击标签栏。
- **关闭标签页**：点击标签页的 "×"（至少保留一个标签页）。
- **地址栏导航**：在地址栏输入 URL 后按回车键。

## 许可证

本项目基于 **GNU通用公共许可证 v3.0** 开源。  
详见 [LICENSE](LICENSE) 文件。

## 参与贡献

欢迎贡献代码！  
1. Fork 本仓库。  
2. 创建功能分支：`git checkout -b feature/新功能名称`。  
3. 提交代码：`git commit -m "添加新功能描述"`。  
4. 推送分支：`git push origin feature/新功能名称`。  
5. 提交 Pull Request。

## 联系方式

- **开发者**：Helloworldpxy
- **GitHub**：[https://github.com/helloworldpxy](https://github.com/helloworldpxy)
- **邮箱**：[hklpl@icloud.com](mailto:hklpl@icloud.com)

## 致谢

- 基于 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 和 [QtWebEngine](https://doc.qt.io/qt-5/qtwebengine-index.html) 构建。
- 图标来源 [Flaticon](https://www.flaticon.com/)（如需署名请补充说明）。

---

🐞 提交问题至 [Issues](https://github.com/helloworldpxy/pybrowser/issues)。  
⭐ 如果觉得项目有用，欢迎 Star 支持！

---

### 注意事项
1. 请确保 `icons` 目录包含以下图标文件（示例需自行补充或替换）：
   - `back.png`（后退）
   - `forward.png`（前进）
   - `stop.png`（停止）
   - `renew.png`（刷新）
   - `add_page.png`（新建标签页）
   - `python.png`（窗口图标）
2. 若图标来源需额外署名，请在 **致谢** 部分补充说明。
3. 快捷键功能（如 `Ctrl+T`）需在代码中实现后更新说明。

## 联系

如有任何问题或建议，请通过以下方式联系：
邮箱：hklpl@icloud.com
GitHub：https://github.com/helloworldpxy
