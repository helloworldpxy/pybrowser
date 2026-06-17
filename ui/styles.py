# ui/styles.py
# PyBrowser v2.5 - 主题管理与样式表集中管理

from PyQt5.QtCore import QObject, pyqtSignal


class DarkTheme:
    """暗色主题配色方案"""
    BACKGROUND_DARK = "#1e1e1e"
    BACKGROUND_MEDIUM = "#2d2d2d"
    BACKGROUND_LIGHT = "#3c3c3c"
    BACKGROUND_LIGHTER = "#505050"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    ACCENT_PRIMARY = "#0078d4"
    ACCENT_HOVER = "#0096ff"
    DANGER = "#d32f2f"
    DANGER_HOVER = "#f44336"
    SUCCESS = "#4CAF50"
    BORDER = "#3c3c3c"
    SECURITY_SAFE = "#4CAF50"
    SECURITY_UNSAFE = "#f44336"


class LightTheme:
    """亮色主题配色方案"""
    BACKGROUND_DARK = "#f5f5f5"
    BACKGROUND_MEDIUM = "#ffffff"
    BACKGROUND_LIGHT = "#e8e8e8"
    BACKGROUND_LIGHTER = "#d0d0d0"
    TEXT_PRIMARY = "#1e1e1e"
    TEXT_SECONDARY = "#555555"
    ACCENT_PRIMARY = "#0078d4"
    ACCENT_HOVER = "#005a9e"
    DANGER = "#d32f2f"
    DANGER_HOVER = "#b71c1c"
    SUCCESS = "#2e7d32"
    BORDER = "#cccccc"
    SECURITY_SAFE = "#2e7d32"
    SECURITY_UNSAFE = "#d32f2f"


class ThemeManager(QObject):
    """主题管理器，负责主题切换和样式表生成"""
    
    theme_changed = pyqtSignal(str)  # 'dark' or 'light'
    
    _instance = None
    
    def __init__(self):
        super().__init__()
        self._theme = DarkTheme()
        self._theme_name = 'dark'
    
    @classmethod
    def instance(cls) -> 'ThemeManager':
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = ThemeManager()
        return cls._instance
    
    @property
    def theme(self):
        """获取当前主题配色"""
        return self._theme
    
    @property
    def theme_name(self) -> str:
        """获取当前主题名称"""
        return self._theme_name
    
    def set_theme(self, name: str):
        """设置主题"""
        if name == self._theme_name:
            return
        
        if name == 'light':
            self._theme = LightTheme()
            self._theme_name = 'light'
        else:
            self._theme = DarkTheme()
            self._theme_name = 'dark'
        
        self.theme_changed.emit(self._theme_name)
    
    def toggle_theme(self):
        """切换主题"""
        new_name = 'light' if self._theme_name == 'dark' else 'dark'
        self.set_theme(new_name)
    
    def is_dark(self) -> bool:
        """是否为暗色主题"""
        return self._theme_name == 'dark'
    
    # ---------- 样式表生成方法 ----------
    
    def main_window(self) -> str:
        """主窗口样式"""
        t = self._theme
        return f"""
            QMainWindow {{
                background-color: {t.BACKGROUND_DARK};
            }}
        """
    
    def tab_widget(self) -> str:
        """标签页控件样式"""
        t = self._theme
        return f"""
            QTabWidget::pane {{
                border: 1px solid {t.BORDER};
                background-color: {t.BACKGROUND_MEDIUM};
            }}
            QTabBar::tab {{
                background-color: {t.BACKGROUND_LIGHT};
                color: {t.TEXT_PRIMARY};
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {t.ACCENT_PRIMARY};
                color: #ffffff;
            }}
            QTabBar::tab:hover {{
                background-color: {t.BACKGROUND_LIGHTER};
            }}
        """
    
    def toolbar(self) -> str:
        """工具栏样式"""
        t = self._theme
        return f"""
            QToolBar {{
                background-color: {t.BACKGROUND_MEDIUM};
                padding: 4px;
                border-bottom: 1px solid {t.BORDER};
            }}
            QToolButton {{
                background-color: transparent;
                border: none;
                padding: 6px;
                border-radius: 4px;
                color: {t.TEXT_PRIMARY};
            }}
            QToolButton:hover {{
                background-color: {t.BACKGROUND_LIGHTER};
            }}
            QToolButton:checked {{
                background-color: {t.ACCENT_PRIMARY};
                color: #ffffff;
            }}
        """
    
    def url_bar(self) -> str:
        """地址栏样式"""
        t = self._theme
        return f"""
            QLineEdit {{
                background-color: {t.BACKGROUND_LIGHT};
                color: {t.TEXT_PRIMARY};
                border: 1px solid {t.BACKGROUND_LIGHTER};
                border-radius: 16px;
                padding: 6px 12px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {t.ACCENT_PRIMARY};
            }}
        """
    
    def sidebar(self) -> str:
        """侧边栏样式"""
        t = self._theme
        return f"""
            QListWidget {{
                background-color: {t.BACKGROUND_MEDIUM};
                color: {t.TEXT_PRIMARY};
                border: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {t.BORDER};
            }}
            QListWidget::item:hover {{
                background-color: {t.BACKGROUND_LIGHTER};
            }}
            QListWidget::item:selected {{
                background-color: {t.ACCENT_PRIMARY};
                color: #ffffff;
            }}
        """
    
    def progress_bar(self) -> str:
        """进度条样式"""
        t = self._theme
        return f"""
            QProgressBar {{
                border: none;
                background-color: {t.BACKGROUND_LIGHT};
                border-radius: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {t.ACCENT_PRIMARY};
                border-radius: 8px;
            }}
        """
    
    def button_primary(self) -> str:
        """主要按钮样式"""
        t = self._theme
        return f"""
            QPushButton {{
                background-color: {t.ACCENT_PRIMARY};
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {t.ACCENT_HOVER};
            }}
        """
    
    def button_danger(self) -> str:
        """危险按钮样式"""
        t = self._theme
        return f"""
            QPushButton {{
                background-color: {t.DANGER};
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {t.DANGER_HOVER};
            }}
        """
    
    def dialog(self) -> str:
        """对话框样式"""
        t = self._theme
        return f"""
            QDialog {{
                background-color: {t.BACKGROUND_DARK};
                color: {t.TEXT_PRIMARY};
            }}
            QGroupBox {{
                color: {t.TEXT_PRIMARY};
                border: 1px solid {t.BORDER};
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 16px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QLabel {{
                color: {t.TEXT_PRIMARY};
            }}
            QLineEdit {{
                background-color: {t.BACKGROUND_LIGHT};
                color: {t.TEXT_PRIMARY};
                border: 1px solid {t.BORDER};
                border-radius: 4px;
                padding: 4px 8px;
            }}
            QSpinBox {{
                background-color: {t.BACKGROUND_LIGHT};
                color: {t.TEXT_PRIMARY};
                border: 1px solid {t.BORDER};
                border-radius: 4px;
                padding: 4px 8px;
            }}
        """
    
    def statusbar(self) -> str:
        """状态栏样式"""
        t = self._theme
        return f"""
            QStatusBar {{
                background-color: {t.BACKGROUND_MEDIUM};
                color: {t.TEXT_SECONDARY};
                border-top: 1px solid {t.BORDER};
            }}
        """
    
    def dock_widget(self) -> str:
        """停靠窗口样式"""
        t = self._theme
        return f"""
            QDockWidget {{
                color: {t.TEXT_PRIMARY};
                titlebar-close-icon: none;
            }}
            QDockWidget::title {{
                background-color: {t.BACKGROUND_MEDIUM};
                padding: 6px;
                border-bottom: 1px solid {t.BORDER};
            }}
        """
    
    def splash_screen(self) -> dict:
        """启动画面配色"""
        t = self._theme
        return {
            'background': t.BACKGROUND_DARK,
            'text': t.TEXT_PRIMARY,
            'accent': t.ACCENT_PRIMARY,
            'progress_bg': t.BACKGROUND_LIGHT,
        }


# 兼容旧代码的静态引用（指向 ThemeManager 实例方法）
class Styles:
    """兼容层：将静态属性转发到 ThemeManager"""
    
    @classmethod
    def _tm(cls):
        return ThemeManager.instance()
    
    @classmethod
    def main_window(cls) -> str:
        return cls._tm().main_window()
    
    @classmethod
    def tab_widget(cls) -> str:
        return cls._tm().tab_widget()
    
    @classmethod
    def toolbar(cls) -> str:
        return cls._tm().toolbar()
    
    @classmethod
    def url_bar(cls) -> str:
        return cls._tm().url_bar()
    
    @classmethod
    def sidebar(cls) -> str:
        return cls._tm().sidebar()
    
    @classmethod
    def progress_bar(cls) -> str:
        return cls._tm().progress_bar()
    
    @classmethod
    def button_primary(cls) -> str:
        return cls._tm().button_primary()
    
    @classmethod
    def button_danger(cls) -> str:
        return cls._tm().button_danger()
    
    @classmethod
    def dialog(cls) -> str:
        return cls._tm().dialog()
