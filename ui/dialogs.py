# ui/dialogs.py
# PyBrowser v2.5 - 对话框组件

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QLabel, QLineEdit, QSpinBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import QUrl

from .styles import ThemeManager


class SettingsDialog(QDialog):
    """设置对话框"""
    
    settings_saved = pyqtSignal(dict)
    
    def __init__(self, version: str, build_date: str, current_settings: dict, parent=None):
        super().__init__(parent)
        self.version = version
        self.build_date = build_date
        self.current_settings = current_settings
        self._theme_manager = ThemeManager.instance()
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        tm = self._theme_manager
        self.setWindowTitle(f"设置 - PyBrowser v{self.version}")
        self.setFixedSize(500, 400)
        self.setStyleSheet(tm.dialog())
        
        layout = QVBoxLayout(self)
        
        # 版本信息
        info_group = QGroupBox("关于")
        info_layout = QVBoxLayout()
        
        info_text = f"""
        <h3>PyBrowser v{self.version}</h3>
        <p>构建日期: {self.build_date}</p>
        <p>开发者: <a href="https://github.com/helloworldpxy">helloworldpxy</a></p>
        <p>GitHub: <a href="https://github.com/helloworldpxy/pybrowser">https://github.com/helloworldpxy/pybrowser</a></p>
        <p>© 2026 helloworldpxy. All rights reserved.</p>
        """
        info_label = QLabel(info_text)
        info_label.setOpenExternalLinks(True)
        info_layout.addWidget(info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 设置选项
        settings_group = QGroupBox("浏览器设置")
        settings_layout = QFormLayout()
        
        # 主页设置
        self.homepage_edit = QLineEdit(self.current_settings.get('homepage', 'https://www.google.com'))
        settings_layout.addRow("主页:", self.homepage_edit)
        
        # 历史记录设置
        self.history_spin = QSpinBox()
        self.history_spin.setRange(10, 200)
        self.history_spin.setValue(self.current_settings.get('max_history', 50))
        settings_layout.addRow("历史记录最大数量:", self.history_spin)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("保存设置")
        save_btn.setStyleSheet(tm.button_primary())
        save_btn.clicked.connect(self._on_save)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def _on_save(self):
        """保存设置"""
        settings = {
            'homepage': self.homepage_edit.text(),
            'max_history': self.history_spin.value()
        }
        self.settings_saved.emit(settings)
        QMessageBox.information(self, "成功", "设置已保存！")
        self.accept()


class BookmarkManagerDialog(QDialog):
    """书签管理对话框"""
    
    bookmarks_updated = pyqtSignal(list)
    
    def __init__(self, bookmarks: list, parent=None):
        super().__init__(parent)
        self.bookmarks = bookmarks.copy()
        self._theme_manager = ThemeManager.instance()
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        tm = self._theme_manager
        self.setWindowTitle("管理书签")
        self.setMinimumSize(600, 400)
        self.setStyleSheet(tm.dialog())
        
        layout = QVBoxLayout(self)
        
        # 书签列表
        self.list_widget = QListWidget()
        self._refresh_list()
        layout.addWidget(self.list_widget)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        delete_btn = QPushButton("删除选中")
        delete_btn.setStyleSheet(tm.button_danger())
        delete_btn.clicked.connect(self._on_delete_selected)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def _refresh_list(self):
        """刷新列表显示"""
        self.list_widget.clear()
        for i, bookmark in enumerate(self.bookmarks):
            item = QListWidgetItem(f"{i+1}. {bookmark['title']} - {bookmark['url']}")
            item.setData(Qt.UserRole, i)
            self.list_widget.addItem(item)
    
    def _on_delete_selected(self):
        """删除选中的书签"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        
        # 获取选中的索引
        indices = [item.data(Qt.UserRole) for item in selected_items]
        
        # 从后往前删除
        for i in sorted(indices, reverse=True):
            if i < len(self.bookmarks):
                self.bookmarks.pop(i)
        
        # 刷新列表
        self._refresh_list()
        
        # 发送更新信号
        self.bookmarks_updated.emit(self.bookmarks)
