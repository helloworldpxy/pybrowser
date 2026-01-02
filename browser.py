# browser.py - PyBrowser v2.0
# 开发日期: 2026-01-02
# 开发者: HelloWorld05
# GitHub: https://github.com/helloworldpxy/pybrowser

import sys
import os
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import json
import time

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = "2.0"
        self.build_date = "2026-01-02"
        
        # 历史记录和书签
        self.history = []
        self.max_history = 50
        self.bookmarks = []
        self.load_bookmarks()
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle(f"PyBrowser v{self.version}")
        self.setWindowIcon(QIcon.fromTheme("web-browser") if QIcon.hasThemeIcon("web-browser") else QIcon())
        self.setGeometry(100, 100, 1400, 800)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                background-color: #323232;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #505050;
            }
        """)
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 创建标签页控件
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.main_layout.addWidget(self.tabs)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.create_statusbar()
        
        # 创建侧边栏（书签/历史记录）
        self.create_sidebar()
        
        # 创建第一个标签页
        self.add_new_tab(QUrl("https://www.google.com"), "主页")
        
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #323232;
                padding: 4px;
                border-bottom: 1px solid #3c3c3c;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 6px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #505050;
                border-radius: 16px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        self.addToolBar(toolbar)
        
        # 后退按钮
        self.back_btn = QToolButton()
        self.back_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.back_btn.setToolTip("后退")
        toolbar.addWidget(self.back_btn)
        
        # 前进按钮
        self.forward_btn = QToolButton()
        self.forward_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.forward_btn.setToolTip("前进")
        toolbar.addWidget(self.forward_btn)
        
        # 刷新按钮
        self.reload_btn = QToolButton()
        self.reload_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.reload_btn.setToolTip("刷新")
        toolbar.addWidget(self.reload_btn)
        
        # 主页按钮
        self.home_btn = QToolButton()
        self.home_btn.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        self.home_btn.setToolTip("主页")
        toolbar.addWidget(self.home_btn)
        
        toolbar.addSeparator()
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        
        # 书签按钮
        self.bookmark_btn = QToolButton()
        self.bookmark_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.bookmark_btn.setToolTip("添加书签")
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        toolbar.addWidget(self.bookmark_btn)
        
        # 新标签页按钮
        self.new_tab_btn = QToolButton()
        self.new_tab_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.new_tab_btn.setToolTip("新标签页")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        toolbar.addWidget(self.new_tab_btn)
        
        # 侧边栏切换按钮
        self.sidebar_btn = QToolButton()
        self.sidebar_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.sidebar_btn.setToolTip("显示/隐藏侧边栏")
        self.sidebar_btn.setCheckable(True)
        self.sidebar_btn.setChecked(True)
        self.sidebar_btn.toggled.connect(self.toggle_sidebar)
        toolbar.addWidget(self.sidebar_btn)
        
        # 设置按钮
        self.settings_btn = QToolButton()
        self.settings_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.settings_btn.setToolTip("设置")
        self.settings_btn.clicked.connect(self.show_settings)
        toolbar.addWidget(self.settings_btn)
        
    def create_statusbar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMaximumHeight(16)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #3c3c3c;
                border-radius: 8px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 8px;
            }
        """)
        
        # 安全状态标签
        self.security_label = QLabel("安全")
        self.security_label.setStyleSheet("color: #4CAF50; padding: 0 10px;")
        
        self.status_bar.addPermanentWidget(self.security_label)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
    def create_sidebar(self):
        """创建侧边栏"""
        self.sidebar = QDockWidget("侧边栏", self)
        self.sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sidebar.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.sidebar.setMinimumWidth(300)
        
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        
        # 创建标签页
        self.sidebar_tabs = QTabWidget()
        
        # 书签页面
        self.bookmark_list = QListWidget()
        self.bookmark_list.setStyleSheet("""
            QListWidget {
                background-color: #323232;
                color: white;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3c3c3c;
            }
            QListWidget::item:hover {
                background-color: #505050;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
        """)
        self.bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        
        # 历史记录页面
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(self.bookmark_list.styleSheet())
        self.history_list.itemDoubleClicked.connect(self.open_history)
        
        self.sidebar_tabs.addTab(self.bookmark_list, "书签")
        self.sidebar_tabs.addTab(self.history_list, "历史记录")
        
        sidebar_layout.addWidget(self.sidebar_tabs)
        
        # 侧边栏按钮
        btn_layout = QHBoxLayout()
        clear_history_btn = QPushButton("清除历史")
        clear_history_btn.clicked.connect(self.clear_history)
        clear_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f44336;
            }
        """)
        
        manage_bookmarks_btn = QPushButton("管理书签")
        manage_bookmarks_btn.clicked.connect(self.manage_bookmarks)
        manage_bookmarks_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0096ff;
            }
        """)
        
        btn_layout.addWidget(clear_history_btn)
        btn_layout.addWidget(manage_bookmarks_btn)
        sidebar_layout.addLayout(btn_layout)
        
        self.sidebar.setWidget(sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
        
    def add_new_tab(self, qurl=None, label="新标签页"):
        """添加新标签页"""
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        # 连接信号
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadProgress.connect(lambda p, browser=browser: self.update_progress(p, browser))
        browser.loadFinished.connect(lambda ok, browser=browser: self.update_title(browser))
        
        return browser
        
    def setup_connections(self):
        """设置信号连接"""
        # 标签页相关
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        
        # 按钮点击事件
        self.back_btn.clicked.connect(lambda: self.current_browser().back())
        self.forward_btn.clicked.connect(lambda: self.current_browser().forward())
        self.reload_btn.clicked.connect(lambda: self.current_browser().reload())
        self.home_btn.clicked.connect(self.navigate_home)
        
    def current_browser(self):
        """获取当前标签页的浏览器实例"""
        return self.tabs.currentWidget()
        
    def navigate_to_url(self):
        """导航到地址栏中的URL"""
        url = self.url_bar.text()
        
        # 如果不是完整的URL，添加https://前缀
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        self.current_browser().setUrl(QUrl(url))
        self.add_to_history(url)
        
    def navigate_home(self):
        """导航到主页"""
        self.current_browser().setUrl(QUrl("https://www.google.com"))
        
    def update_urlbar(self, q, browser=None):
        """更新地址栏"""
        if browser != self.current_browser():
            return
            
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
        
        # 更新安全状态
        if q.scheme() == 'https':
            self.security_label.setText("安全")
            self.security_label.setStyleSheet("color: #4CAF50; padding: 0 10px;")
        else:
            self.security_label.setText("不安全")
            self.security_label.setStyleSheet("color: #f44336; padding: 0 10px;")
            
    def update_progress(self, progress, browser=None):
        """更新进度条"""
        if browser != self.current_browser():
            return
            
        if progress < 100:
            self.progress_bar.setValue(progress)
            self.progress_bar.show()
        else:
            self.progress_bar.hide()
            
    def update_title(self, browser):
        """更新标签页标题"""
        idx = self.tabs.indexOf(browser)
        title = browser.page().title()
        
        # 限制标题长度
        if len(title) > 20:
            title = title[:20] + "..."
            
        self.tabs.setTabText(idx, title)
        
    def current_tab_changed(self, i):
        """当前标签页改变时更新UI"""
        if i != -1:
            browser = self.current_browser()
            self.update_urlbar(browser.url(), browser)
            self.update_title(browser)
            
    def close_current_tab(self, i):
        """关闭当前标签页"""
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
            
    def toggle_sidebar(self, checked):
        """显示/隐藏侧边栏"""
        self.sidebar.setVisible(checked)
        
    def add_to_history(self, url):
        """添加到历史记录"""
        history_item = {
            'url': url,
            'title': self.current_browser().page().title(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.history.insert(0, history_item)
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        self.update_history_list()
        
    def update_history_list(self):
        """更新历史记录列表"""
        self.history_list.clear()
        for item in self.history:
            list_item = QListWidgetItem(f"{item['title']}\n{item['url']}\n{item['timestamp']}")
            self.history_list.addItem(list_item)
            
    def clear_history(self):
        """清除历史记录"""
        reply = QMessageBox.question(self, '确认', '确定要清除所有历史记录吗？',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history.clear()
            self.update_history_list()
            
    def add_bookmark(self):
        """添加书签"""
        current_url = self.current_browser().url().toString()
        current_title = self.current_browser().page().title()
        
        bookmark = {
            'url': current_url,
            'title': current_title,
            'added': datetime.now().strftime("%Y-%m-%d")
        }
        
        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        self.update_bookmark_list()
        
        QMessageBox.information(self, "成功", "书签已添加！")
        
    def update_bookmark_list(self):
        """更新书签列表"""
        self.bookmark_list.clear()
        for bookmark in self.bookmarks:
            list_item = QListWidgetItem(f"{bookmark['title']}\n{bookmark['url']}")
            self.bookmark_list.addItem(list_item)
            
    def open_bookmark(self, item):
        """打开书签"""
        text = item.text().split('\n')
        url = text[1] if len(text) > 1 else text[0]
        self.current_browser().setUrl(QUrl(url))
        
    def open_history(self, item):
        """打开历史记录"""
        text = item.text().split('\n')
        url = text[1] if len(text) > 1 else text[0]
        self.current_browser().setUrl(QUrl(url))
        
    def load_bookmarks(self):
        """加载书签"""
        try:
            with open('bookmarks.json', 'r', encoding='utf-8') as f:
                self.bookmarks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.bookmarks = []
            
    def save_bookmarks(self):
        """保存书签"""
        with open('bookmarks.json', 'w', encoding='utf-8') as f:
            json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
            
    def manage_bookmarks(self):
        """管理书签对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("管理书签")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 书签列表
        list_widget = QListWidget()
        for i, bookmark in enumerate(self.bookmarks):
            item = QListWidgetItem(f"{i+1}. {bookmark['title']} - {bookmark['url']}")
            item.setData(Qt.UserRole, i)
            list_widget.addItem(item)
            
        layout.addWidget(list_widget)
        
        # 按钮
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("删除选中")
        delete_btn.clicked.connect(lambda: self.delete_selected_bookmark(list_widget))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f44336;
            }
        """)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec_()
        
    def delete_selected_bookmark(self, list_widget):
        """删除选中的书签"""
        selected_items = list_widget.selectedItems()
        if not selected_items:
            return
            
        indices = [item.data(Qt.UserRole) for item in selected_items]
        
        # 从后往前删除
        for i in sorted(indices, reverse=True):
            if i < len(self.bookmarks):
                self.bookmarks.pop(i)
                
        self.save_bookmarks()
        self.update_bookmark_list()
        
        # 重新加载对话框
        self.manage_bookmarks()
        
    def show_settings(self):
        """显示设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"设置 - PyBrowser v{self.version}")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 版本信息
        info_group = QGroupBox("关于")
        info_layout = QVBoxLayout()
        
        info_text = f"""
        <h3>PyBrowser v{self.version}</h3>
        <p>构建日期: {self.build_date}</p>
        <p>开发者: HelloWorld05</p>
        <p>GitHub: <a href="https://github.com/helloworldpxy/pybrowser">https://github.com/helloworldpxy/pybrowser</a></p>
        <p>© 2026 HelloWorld05. All rights reserved.</p>
        """
        info_label = QLabel(info_text)
        info_label.setOpenExternalLinks(True)
        info_layout.addWidget(info_label)
        info_group.setLayout(info_layout)
        
        # 设置选项
        settings_group = QGroupBox("浏览器设置")
        settings_layout = QFormLayout()
        
        # 主页设置
        self.homepage_edit = QLineEdit("https://www.google.com")
        settings_layout.addRow("主页:", self.homepage_edit)
        
        # 历史记录设置
        self.history_spin = QSpinBox()
        self.history_spin.setRange(10, 200)
        self.history_spin.setValue(self.max_history)
        settings_layout.addRow("历史记录最大数量:", self.history_spin)
        
        settings_group.setLayout(settings_layout)
        
        layout.addWidget(info_group)
        layout.addWidget(settings_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存设置")
        save_btn.clicked.connect(lambda: self.save_settings(dialog))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0096ff;
            }
        """)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec_()
        
    def save_settings(self, dialog):
        """保存设置"""
        self.max_history = self.history_spin.value()
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            self.update_history_list()
            
        QMessageBox.information(self, "成功", "设置已保存！")
        dialog.accept()
        
    def closeEvent(self, event):
        """关闭事件"""
        self.save_bookmarks()
        event.accept()

class SplashScreen(QSplashScreen):
    """启动画面"""
    def __init__(self):
        # 先设置窗口标志，然后创建父类
        super().__init__()
        
        # 设置窗口标志 - 正确的写法
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # 创建一个图像作为启动画面
        pixmap = QPixmap(600, 300)
        pixmap.fill(QColor("#2b2b2b"))
        
        # 绘制内容
        painter = QPainter(pixmap)
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "PyBrowser")
        
        painter.setFont(QFont("Arial", 12))
        painter.drawText(pixmap.rect().adjusted(0, 100, 0, 0), Qt.AlignCenter, "版本 2.0")
        
        painter.setFont(QFont("Arial", 10))
        painter.drawText(pixmap.rect().adjusted(0, 140, 0, 0), Qt.AlignCenter, "正在加载...")
        
        painter.setPen(QColor("#0078d4"))
        painter.setBrush(QColor("#0078d4"))
        
        # 简单的进度条
        progress_width = 400
        progress_height = 10
        x = (pixmap.width() - progress_width) // 2
        y = pixmap.height() - 80
        
        painter.drawRect(x, y, progress_width, progress_height)
        painter.end()
        
        # 设置启动画面的图像
        self.setPixmap(pixmap)
        
    def show_message(self, message):
        """显示消息"""
        self.showMessage(message, Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyBrowser")
    app.setApplicationVersion("2.0")
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 创建并显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 模拟加载过程
    splash.showMessage("正在初始化... (1/5)", Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))
    app.processEvents()
    time.sleep(0.1)
    
    splash.showMessage("正在初始化... (2/5)", Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))
    app.processEvents()
    time.sleep(0.1)
    
    splash.showMessage("正在初始化... (3/5)", Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))
    app.processEvents()
    time.sleep(0.1)
    
    splash.showMessage("正在初始化... (4/5)", Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))
    app.processEvents()
    time.sleep(0.1)
    
    splash.showMessage("正在初始化... (5/5)", Qt.AlignBottom | Qt.AlignHCenter, QColor("#ffffff"))
    app.processEvents()
    time.sleep(0.1)
    
    # 创建主窗口
    window = BrowserWindow()
    
    # 关闭启动画面并显示主窗口
    time.sleep(0.5)
    splash.finish(window)
    window.show()
    
    # 显示欢迎消息
    QTimer.singleShot(1000, lambda: QMessageBox.information(
        window, "欢迎", 
        f"欢迎使用 PyBrowser v{window.version}！\n"
        f"新功能：\n"
        f"• 现代化的暗色主题界面\n"
        f"• 多标签页浏览\n"
        f"• 书签管理\n"
        f"• 浏览历史记录\n"
        f"• 可自定义设置\n\n"
        f"构建日期：{window.build_date}\n"
        f"开发者：HelloWorld05"
    ))
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()