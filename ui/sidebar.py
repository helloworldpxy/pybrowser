# ui/sidebar.py
# PyBrowser v2.5 - 侧边栏组件

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QListWidget, QListWidgetItem, QPushButton
)

from .styles import ThemeManager


class Sidebar(QWidget):
    """侧边栏，包含书签和历史记录"""
    
    # 自定义信号
    bookmark_selected = pyqtSignal(str)  # URL
    history_selected = pyqtSignal(str)  # URL
    clear_history_requested = pyqtSignal()
    manage_bookmarks_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager.instance()
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        tm = self._theme_manager
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页控件
        self.tabs = QTabWidget()
        
        # 书签页面
        self.bookmark_list = QListWidget()
        self.bookmark_list.setStyleSheet(tm.sidebar())
        self.bookmark_list.itemDoubleClicked.connect(self._on_bookmark_double_clicked)
        self.tabs.addTab(self.bookmark_list, "书签")
        
        # 历史记录页面
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(tm.sidebar())
        self.history_list.itemDoubleClicked.connect(self._on_history_double_clicked)
        self.tabs.addTab(self.history_list, "历史记录")
        
        layout.addWidget(self.tabs)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        
        # 清除历史按钮
        clear_btn = QPushButton("清除历史")
        clear_btn.setStyleSheet(tm.button_danger())
        clear_btn.clicked.connect(self.clear_history_requested.emit)
        btn_layout.addWidget(clear_btn)
        
        # 管理书签按钮
        manage_btn = QPushButton("管理书签")
        manage_btn.setStyleSheet(tm.button_primary())
        manage_btn.clicked.connect(self.manage_bookmarks_requested.emit)
        btn_layout.addWidget(manage_btn)
        
        layout.addLayout(btn_layout)
    
    def _on_bookmark_double_clicked(self, item: QListWidgetItem):
        """书签双击处理"""
        text = item.text()
        # 从 "标题\nURL" 格式中提取 URL
        lines = text.split('\n')
        url = lines[1] if len(lines) > 1 else lines[0]
        self.bookmark_selected.emit(url)
    
    def _on_history_double_clicked(self, item: QListWidgetItem):
        """历史记录双击处理"""
        text = item.text()
        lines = text.split('\n')
        url = lines[1] if len(lines) > 1 else lines[0]
        self.history_selected.emit(url)
    
    def update_bookmarks(self, bookmarks: list):
        """更新书签列表"""
        self.bookmark_list.clear()
        for bookmark in bookmarks:
            text = f"{bookmark['title']}\n{bookmark['url']}"
            self.bookmark_list.addItem(QListWidgetItem(text))
    
    def update_history(self, history: list):
        """更新历史记录列表"""
        self.history_list.clear()
        for item in history:
            text = f"{item['title']}\n{item['url']}\n{item['timestamp']}"
            self.history_list.addItem(QListWidgetItem(text))
    
    def apply_theme(self):
        """应用当前主题样式"""
        tm = self._theme_manager
        self.bookmark_list.setStyleSheet(tm.sidebar())
        self.history_list.setStyleSheet(tm.sidebar())


class SidebarDock(QDockWidget):
    """侧边栏停靠窗口"""
    
    def __init__(self, parent=None):
        super().__init__("侧边栏", parent)
        self._theme_manager = ThemeManager.instance()
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        from PyQt5.QtCore import Qt
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(
            self.DockWidgetMovable | self.DockWidgetFloatable
        )
        self.setMinimumWidth(300)
        
        # 创建侧边栏内容
        self.sidebar = Sidebar()
        self.setWidget(self.sidebar)
    
    def apply_theme(self):
        """应用当前主题样式"""
        tm = self._theme_manager
        self.setStyleSheet(tm.dock_widget())
        self.sidebar.apply_theme()
