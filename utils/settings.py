# utils/settings.py
# PyBrowser v2.5 - 设置管理

import json
from pathlib import Path
from typing import Dict, Any


class SettingsManager:
    """设置管理器，负责应用程序设置的持久化存储"""
    
    # 默认设置
    DEFAULT_SETTINGS = {
        'homepage': 'https://www.google.com',
        'max_history': 50,
        'window_geometry': None,  # 窗口位置和大小
        'sidebar_visible': True,
        'last_visited': None,
        'theme': 'dark'  # 主题：dark 或 light
    }
    
    def __init__(self):
        self._settings: Dict[str, Any] = {}
        self._config_dir = self._get_config_dir()
        self._settings_file = self._config_dir / "settings.json"
        
        # 确保配置目录存在
        self._config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载设置
        self._load()
    
    def _get_config_dir(self) -> Path:
        """获取配置目录"""
        home = Path.home()
        return home / ".pybrowser"
    
    def _load(self):
        """从文件加载设置"""
        try:
            if self._settings_file.exists():
                with open(self._settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # 合并默认设置和加载的设置
                    self._settings = {**self.DEFAULT_SETTINGS, **loaded}
            else:
                self._settings = self.DEFAULT_SETTINGS.copy()
        except (json.JSONDecodeError, IOError):
            self._settings = self.DEFAULT_SETTINGS.copy()
    
    def _save(self):
        """保存设置到文件"""
        try:
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=2)
        except IOError:
            pass  # 静默处理写入错误
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置值"""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置值"""
        self._settings[key] = value
        self._save()
    
    def update(self, settings: Dict[str, Any]):
        """批量更新设置"""
        self._settings.update(settings)
        self._save()
    
    def get_homepage(self) -> str:
        """获取主页 URL"""
        return self._settings.get('homepage', 'https://www.google.com')
    
    def set_homepage(self, url: str):
        """设置主页 URL"""
        self._settings['homepage'] = url
        self._save()
    
    def get_max_history(self) -> int:
        """获取最大历史记录数量"""
        return self._settings.get('max_history', 50)
    
    def set_max_history(self, max_items: int):
        """设置最大历史记录数量"""
        self._settings['max_history'] = max_items
        self._save()
    
    def get_window_geometry(self):
        """获取窗口几何信息"""
        return self._settings.get('window_geometry')
    
    def set_window_geometry(self, geometry):
        """设置窗口几何信息"""
        self._settings['window_geometry'] = geometry
        self._save()
    
    def is_sidebar_visible(self) -> bool:
        """获取侧边栏可见性"""
        return self._settings.get('sidebar_visible', True)
    
    def set_sidebar_visible(self, visible: bool):
        """设置侧边栏可见性"""
        self._settings['sidebar_visible'] = visible
        self._save()
    
    def get_theme(self) -> str:
        """获取主题设置"""
        return self._settings.get('theme', 'dark')
    
    def set_theme(self, theme: str):
        """设置主题"""
        self._settings['theme'] = theme
        self._save()
