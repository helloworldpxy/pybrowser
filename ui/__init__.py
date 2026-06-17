# ui/__init__.py
# PyBrowser v2.5 - 用户界面模块

from .toolbar import NavigationToolbar
from .sidebar import Sidebar, SidebarDock
from .dialogs import SettingsDialog, BookmarkManagerDialog
from .styles import Styles, ThemeManager, DarkTheme, LightTheme

__all__ = ['NavigationToolbar', 'Sidebar', 'SidebarDock', 'SettingsDialog', 'BookmarkManagerDialog', 'Styles', 'ThemeManager', 'DarkTheme', 'LightTheme']
