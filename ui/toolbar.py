# ui/toolbar.py
# PyBrowser v2.5 - 导航工具栏

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QToolBar, QToolButton, QLineEdit, QStyle, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QIcon

from .styles import ThemeManager


class NavigationToolbar(QWidget):
    """导航工具栏，包含前进、后退、刷新、主页、地址栏等"""
    
    # 自定义信号
    back_requested = pyqtSignal()
    forward_requested = pyqtSignal()
    reload_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    home_requested = pyqtSignal()
    navigate_requested = pyqtSignal(str)
    bookmark_requested = pyqtSignal()
    new_tab_requested = pyqtSignal()
    sidebar_toggle_requested = pyqtSignal(bool)
    settings_requested = pyqtSignal()
    theme_toggle_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_manager = ThemeManager.instance()
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # 后退按钮
        self.back_btn = self._create_button("后退", QStyle.SP_ArrowBack)
        self.back_btn.clicked.connect(self.back_requested.emit)
        layout.addWidget(self.back_btn)
        
        # 前进按钮
        self.forward_btn = self._create_button("前进", QStyle.SP_ArrowForward)
        self.forward_btn.clicked.connect(self.forward_requested.emit)
        layout.addWidget(self.forward_btn)
        
        # 刷新按钮
        self.reload_btn = self._create_button("刷新", QStyle.SP_BrowserReload)
        self.reload_btn.clicked.connect(self.reload_requested.emit)
        layout.addWidget(self.reload_btn)
        
        # 停止按钮
        self.stop_btn = self._create_button("停止", QStyle.SP_BrowserStop)
        self.stop_btn.clicked.connect(self.stop_requested.emit)
        self.stop_btn.setVisible(False)
        layout.addWidget(self.stop_btn)
        
        # 主页按钮
        self.home_btn = self._create_button("主页", QStyle.SP_DirHomeIcon)
        self.home_btn.clicked.connect(self.home_requested.emit)
        layout.addWidget(self.home_btn)
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索...")
        self.url_bar.setStyleSheet(self._theme_manager.url_bar())
        self.url_bar.returnPressed.connect(self._on_url_bar_return_pressed)
        layout.addWidget(self.url_bar, 1)  # 1 = stretch factor
        
        # 书签按钮
        self.bookmark_btn = self._create_button("添加书签", QStyle.SP_DialogSaveButton)
        self.bookmark_btn.clicked.connect(self.bookmark_requested.emit)
        layout.addWidget(self.bookmark_btn)
        
        # 新标签页按钮
        self.new_tab_btn = self._create_button("新标签页", QStyle.SP_FileDialogNewFolder)
        self.new_tab_btn.clicked.connect(self.new_tab_requested.emit)
        layout.addWidget(self.new_tab_btn)
        
        # 侧边栏切换按钮
        self.sidebar_btn = self._create_button("显示/隐藏侧边栏", QStyle.SP_FileDialogDetailedView)
        self.sidebar_btn.setCheckable(True)
        self.sidebar_btn.setChecked(True)
        self.sidebar_btn.toggled.connect(self.sidebar_toggle_requested.emit)
        layout.addWidget(self.sidebar_btn)
        
        # 设置按钮
        self.settings_btn = self._create_button("设置", QStyle.SP_FileDialogListView)
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(self.settings_btn)
        
        # 主题切换按钮
        self.theme_btn = self._create_button("切换主题", QStyle.SP_FileDialogInfoView)
        self.theme_btn.clicked.connect(self.theme_toggle_requested.emit)
        layout.addWidget(self.theme_btn)
    
    def _create_button(self, tooltip: str, icon_type) -> QToolButton:
        """创建工具栏按钮"""
        btn = QToolButton()
        btn.setIcon(self.style().standardIcon(icon_type))
        btn.setToolTip(tooltip)
        btn.setStyleSheet(self._theme_manager.toolbar())
        return btn
    
    def apply_theme(self):
        """应用当前主题样式"""
        tm = self._theme_manager
        self.setStyleSheet(tm.toolbar())
        self.url_bar.setStyleSheet(tm.url_bar())
        for btn in self.findChildren(QToolButton):
            btn.setStyleSheet(tm.toolbar())
    
    def _on_url_bar_return_pressed(self):
        """地址栏回车处理"""
        url = self.url_bar.text().strip()
        if url:
            self.navigate_requested.emit(url)
    
    def update_url(self, url: str):
        """更新地址栏显示"""
        self.url_bar.setText(url)
        self.url_bar.setCursorPosition(0)
    
    def set_loading_state(self, loading: bool):
        """设置加载状态"""
        self.reload_btn.setVisible(not loading)
        self.stop_btn.setVisible(loading)
