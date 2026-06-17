# main.py
# PyBrowser v2.5 - 主入口文件
# 开发者: helloworldpxy
# GitHub: https://github.com/helloworldpxy/pybrowser
# 许可证: PolyForm Noncommercial License 1.0.0

import sys
import time
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QColor, QFont, QPainter, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QSplashScreen, QMessageBox, QStatusBar, QProgressBar, QLabel,
    QStyle, QShortcut
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

from core import TabManager
from ui import NavigationToolbar, SidebarDock, SettingsDialog, BookmarkManagerDialog, Styles, ThemeManager
from utils import HistoryManager, BookmarkManager, SettingsManager


class BrowserWindow(QMainWindow):
    """PyBrowser 主窗口"""
    
    VERSION = "2.5"
    BUILD_DATE = "2026-06-17"
    
    def __init__(self):
        super().__init__()
        
        # 初始化管理器
        self.settings_manager = SettingsManager()
        self.history_manager = HistoryManager(self.settings_manager.get_max_history())
        self.bookmark_manager = BookmarkManager()
        
        # 初始化主题管理器
        self._theme_manager = ThemeManager.instance()
        saved_theme = self.settings_manager.get_theme()
        self._theme_manager.set_theme(saved_theme)
        
        # 设置窗口属性
        self.setWindowTitle(f"PyBrowser v{self.VERSION}")
        self.setWindowIcon(QIcon.fromTheme("web-browser") if QIcon.hasThemeIcon("web-browser") else QIcon())
        self.setGeometry(100, 100, 1400, 800)
        
        # 设置 UI
        self._setup_ui()
        self._setup_connections()
        self._setup_shortcuts()
        
        # 创建第一个标签页
        homepage = self.settings_manager.get_homepage()
        self.tab_manager.add_tab(QUrl(homepage), "主页")
        
        # 恢复侧边栏状态
        sidebar_visible = self.settings_manager.is_sidebar_visible()
        self.sidebar.setVisible(sidebar_visible)
        self.toolbar.sidebar_btn.setChecked(sidebar_visible)
        
        # 在所有 UI 构建完成后应用主题
        self._apply_theme()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建工具栏
        self.toolbar = NavigationToolbar()
        main_layout.addWidget(self.toolbar)
        
        # 创建标签页控件
        from PyQt5.QtWidgets import QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setStyleSheet(Styles.tab_widget())
        main_layout.addWidget(self.tab_widget)
        
        # 创建标签页管理器
        self.tab_manager = TabManager(self.tab_widget)
        
        # 创建侧边栏
        self.sidebar = SidebarDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
        
        # 创建状态栏
        self._setup_statusbar()
    
    def _setup_statusbar(self):
        """设置状态栏"""
        tm = self._theme_manager
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMaximumHeight(16)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(tm.progress_bar())
        self.progress_bar.hide()
        
        # 安全状态标签
        self.security_label = QLabel("安全")
        self.security_label.setStyleSheet(f"color: {tm.theme.SECURITY_SAFE}; padding: 0 10px;")
        
        self.status_bar.addPermanentWidget(self.security_label)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def _setup_connections(self):
        """设置信号连接"""
        # 工具栏信号
        self.toolbar.back_requested.connect(self._on_back)
        self.toolbar.forward_requested.connect(self._on_forward)
        self.toolbar.reload_requested.connect(self._on_reload)
        self.toolbar.stop_requested.connect(self._on_stop)
        self.toolbar.home_requested.connect(self._on_home)
        self.toolbar.navigate_requested.connect(self._on_navigate)
        self.toolbar.bookmark_requested.connect(self._on_add_bookmark)
        self.toolbar.new_tab_requested.connect(self._on_new_tab)
        self.toolbar.sidebar_toggle_requested.connect(self._on_toggle_sidebar)
        self.toolbar.settings_requested.connect(self._on_show_settings)
        self.toolbar.theme_toggle_requested.connect(self._on_theme_toggle)
        
        # 标签页管理器信号
        self.tab_manager.current_changed.connect(self._on_current_tab_changed)
        self.tab_manager.title_updated.connect(self._on_title_updated)
        self.tab_manager.url_updated.connect(self._on_url_updated)
        self.tab_manager.load_progress_updated.connect(self._on_load_progress)
        
        # 侧边栏信号
        self.sidebar.sidebar.bookmark_selected.connect(self._on_open_bookmark)
        self.sidebar.sidebar.history_selected.connect(self._on_open_history)
        self.sidebar.sidebar.clear_history_requested.connect(self._on_clear_history)
        self.sidebar.sidebar.manage_bookmarks_requested.connect(self._on_manage_bookmarks)
    
    def _setup_shortcuts(self):
        """设置快捷键"""
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        
        # Ctrl+T: 新标签页
        QShortcut(QKeySequence("Ctrl+T"), self, self._on_new_tab)
        
        # Ctrl+W: 关闭标签页
        QShortcut(QKeySequence("Ctrl+W"), self, self._on_close_current_tab)
        
        # Ctrl+L: 聚焦地址栏
        QShortcut(QKeySequence("Ctrl+L"), self, lambda: self.toolbar.url_bar.setFocus())
        
        # F5: 刷新
        QShortcut(QKeySequence("F5"), self, self._on_reload)
        
        # Ctrl+D: 添加书签
        QShortcut(QKeySequence("Ctrl+D"), self, self._on_add_bookmark)
        
        # Ctrl+Shift+T: 切换主题
        QShortcut(QKeySequence("Ctrl+Shift+T"), self, self._on_theme_toggle)
    
    def _on_back(self):
        """后退"""
        view = self.tab_manager.current_view()
        if view:
            view.back()
    
    def _on_forward(self):
        """前进"""
        view = self.tab_manager.current_view()
        if view:
            view.forward()
    
    def _on_reload(self):
        """刷新"""
        view = self.tab_manager.current_view()
        if view:
            view.reload()
    
    def _on_stop(self):
        """停止加载"""
        view = self.tab_manager.current_view()
        if view:
            view.stop()
    
    def _on_home(self):
        """导航到主页"""
        view = self.tab_manager.current_view()
        if view:
            homepage = self.settings_manager.get_homepage()
            view.navigate_to(homepage)
    
    def _on_navigate(self, url: str):
        """导航到指定 URL"""
        view = self.tab_manager.current_view()
        if view:
            view.navigate_to(url)
            # 添加到历史记录
            self.history_manager.add(url, view.get_title())
            # 更新侧边栏
            self.sidebar.sidebar.update_history(self.history_manager.get_all())
    
    def _on_new_tab(self):
        """新建标签页"""
        homepage = self.settings_manager.get_homepage()
        self.tab_manager.add_tab(QUrl(homepage), "新标签页")
    
    def _on_close_current_tab(self):
        """关闭当前标签页"""
        current_index = self.tab_manager.current_index()
        self.tab_manager.close_tab(current_index)
    
    def _on_add_bookmark(self):
        """添加书签"""
        view = self.tab_manager.current_view()
        if view:
            url = view.get_url()
            title = view.get_title()
            
            if self.bookmark_manager.add(url, title):
                QMessageBox.information(self, "成功", "书签已添加！")
                # 更新侧边栏
                self.sidebar.sidebar.update_bookmarks(self.bookmark_manager.get_all())
            else:
                QMessageBox.information(self, "提示", "该书签已存在！")
    
    def _on_toggle_sidebar(self, visible: bool):
        """切换侧边栏显示"""
        self.sidebar.setVisible(visible)
        self.settings_manager.set_sidebar_visible(visible)
    
    def _on_theme_toggle(self):
        """切换主题"""
        self._theme_manager.toggle_theme()
        self._apply_theme()
        # 保存主题偏好
        self.settings_manager.set_theme(self._theme_manager.theme_name)
    
    def _apply_theme(self):
        """应用当前主题到所有组件"""
        tm = self._theme_manager
        # 主窗口
        self.setStyleSheet(tm.main_window() + tm.tab_widget())
        # 标签页
        self.tab_widget.setStyleSheet(tm.tab_widget())
        # 工具栏
        self.toolbar.apply_theme()
        # 侧边栏
        self.sidebar.apply_theme()
        # 状态栏
        self.status_bar.setStyleSheet(tm.statusbar())
        self.progress_bar.setStyleSheet(tm.progress_bar())
        # 安全标签
        if self._theme_manager.is_dark():
            self.security_label.setStyleSheet(f"color: {tm.theme.SECURITY_SAFE}; padding: 0 10px;")
        else:
            self.security_label.setStyleSheet(f"color: {tm.theme.SECURITY_SAFE}; padding: 0 10px;")
    
    def _on_show_settings(self):
        """显示设置对话框"""
        current_settings = {
            'homepage': self.settings_manager.get_homepage(),
            'max_history': self.settings_manager.get_max_history()
        }
        
        dialog = SettingsDialog(self.VERSION, self.BUILD_DATE, current_settings, self)
        dialog.settings_saved.connect(self._on_settings_saved)
        dialog.exec_()
    
    def _on_settings_saved(self, settings: dict):
        """设置保存处理"""
        self.settings_manager.update(settings)
        self.history_manager.set_max_items(settings.get('max_history', 50))
    
    def _on_current_tab_changed(self, index: int):
        """当前标签页变化处理"""
        view = self.tab_manager.current_view()
        if view:
            # 更新地址栏
            self.toolbar.update_url(view.get_url())
            # 更新安全状态
            self._update_security_status(view.get_url())
    
    def _on_title_updated(self, index: int, title: str):
        """标题更新处理"""
        # 添加到历史记录
        view = self.tab_manager.current_view()
        if view and index == self.tab_manager.current_index():
            url = view.get_url()
            if url and not url.startswith('about:'):
                self.history_manager.add(url, title)
                # 更新侧边栏
                self.sidebar.sidebar.update_history(self.history_manager.get_all())
    
    def _on_url_updated(self, index: int, url: QUrl):
        """URL 更新处理"""
        if index == self.tab_manager.current_index():
            # 更新地址栏
            self.toolbar.update_url(url.toString())
            # 更新安全状态
            self._update_security_status(url.toString())
    
    def _on_load_progress(self, index: int, progress: int):
        """加载进度处理"""
        if index == self.tab_manager.current_index():
            if progress < 100:
                self.progress_bar.setValue(progress)
                self.progress_bar.show()
                self.toolbar.set_loading_state(True)
            else:
                self.progress_bar.hide()
                self.toolbar.set_loading_state(False)
    
    def _on_open_bookmark(self, url: str):
        """打开书签"""
        view = self.tab_manager.current_view()
        if view:
            view.navigate_to(url)
    
    def _on_open_history(self, url: str):
        """打开历史记录"""
        view = self.tab_manager.current_view()
        if view:
            view.navigate_to(url)
    
    def _on_clear_history(self):
        """清除历史记录"""
        reply = QMessageBox.question(
            self, '确认', '确定要清除所有历史记录吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.history_manager.clear()
            self.sidebar.sidebar.update_history([])
    
    def _on_manage_bookmarks(self):
        """管理书签"""
        bookmarks = self.bookmark_manager.get_all()
        dialog = BookmarkManagerDialog(bookmarks, self)
        dialog.bookmarks_updated.connect(self._on_bookmarks_updated)
        dialog.exec_()
    
    def _on_bookmarks_updated(self, bookmarks: list):
        """书签更新处理"""
        self.bookmark_manager.update(bookmarks)
        self.sidebar.sidebar.update_bookmarks(bookmarks)
    
    def _update_security_status(self, url: str):
        """更新安全状态显示"""
        tm = self._theme_manager
        if url.startswith('https://'):
            self.security_label.setText("安全")
            self.security_label.setStyleSheet(f"color: {tm.theme.SECURITY_SAFE}; padding: 0 10px;")
        elif url.startswith('http://'):
            self.security_label.setText("不安全")
            self.security_label.setStyleSheet(f"color: {tm.theme.SECURITY_UNSAFE}; padding: 0 10px;")
        else:
            self.security_label.setText("")
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 保存窗口几何信息
        geometry = self.saveGeometry()
        self.settings_manager.set_window_geometry(geometry.toHex().data().decode())
        event.accept()


class SplashScreen(QSplashScreen):
    """启动画面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self._create_splash()
    
    def _create_splash(self):
        """创建启动画面"""
        tm = ThemeManager.instance()
        colors = tm.splash_screen()
        
        pixmap = QPixmap(600, 300)
        pixmap.fill(QColor(colors['background']))
        
        painter = QPainter(pixmap)
        
        # 标题
        painter.setPen(QColor(colors['text']))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "PyBrowser")
        
        # 版本
        painter.setFont(QFont("Arial", 12))
        painter.drawText(pixmap.rect().adjusted(0, 100, 0, 0), Qt.AlignCenter, "版本 2.5")
        
        # 加载提示
        painter.setFont(QFont("Arial", 10))
        painter.drawText(pixmap.rect().adjusted(0, 140, 0, 0), Qt.AlignCenter, "正在加载...")
        
        # 进度条背景
        painter.setPen(QColor(colors['progress_bg']))
        painter.setBrush(QColor(colors['progress_bg']))
        progress_width = 400
        progress_height = 10
        x = (pixmap.width() - progress_width) // 2
        y = pixmap.height() - 80
        painter.drawRect(x, y, progress_width, progress_height)
        
        # 进度条前景
        painter.setPen(QColor(colors['accent']))
        painter.setBrush(QColor(colors['accent']))
        painter.drawRect(x, y, progress_width // 2, progress_height)
        
        painter.end()
        self.setPixmap(pixmap)
    
    def show_message(self, message: str):
        """显示消息"""
        tm = ThemeManager.instance()
        self.showMessage(message, Qt.AlignBottom | Qt.AlignHCenter, QColor(tm.theme.TEXT_PRIMARY))


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("PyBrowser")
    app.setApplicationVersion("2.5")
    app.setStyle("Fusion")
    
    # 创建并显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 模拟加载过程
    for i in range(1, 6):
        splash.show_message(f"正在初始化... ({i}/5)")
        app.processEvents()
        time.sleep(0.1)
    
    # 创建主窗口
    window = BrowserWindow()
    
    # 关闭启动画面并显示主窗口
    time.sleep(0.3)
    splash.finish(window)
    window.show()
    
    # 显示欢迎消息（延迟显示，避免阻塞启动）
    QTimer.singleShot(1000, lambda: QMessageBox.information(
        window, "欢迎",
        f"欢迎使用 PyBrowser v{window.VERSION}！\n\n"
        f"新功能：\n"
        f"• 模块化架构设计\n"
        f"• 现代化的暗色主题界面\n"
        f"• 多标签页浏览\n"
        f"• 书签管理（数据持久化）\n"
        f"• 浏览历史记录（数据持久化）\n"
        f"• 快捷键支持（Ctrl+T/W/L/D/F5）\n"
        f"• 可自定义设置\n\n"
        f"构建日期：{window.BUILD_DATE}\n"
        f"开发者：helloworldpxy"
    ))
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
