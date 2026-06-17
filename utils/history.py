# utils/history.py
# PyBrowser v2.5 - 历史记录管理

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class HistoryManager:
    """历史记录管理器，负责历史记录的持久化存储"""
    
    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self._history: List[Dict] = []
        self._config_dir = self._get_config_dir()
        self._history_file = self._config_dir / "history.json"
        
        # 确保配置目录存在
        self._config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载历史记录
        self._load()
    
    def _get_config_dir(self) -> Path:
        """获取配置目录"""
        home = Path.home()
        return home / ".pybrowser"
    
    def _load(self):
        """从文件加载历史记录"""
        try:
            if self._history_file.exists():
                with open(self._history_file, 'r', encoding='utf-8') as f:
                    self._history = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._history = []
    
    def _save(self):
        """保存历史记录到文件"""
        try:
            with open(self._history_file, 'w', encoding='utf-8') as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except IOError:
            pass  # 静默处理写入错误
    
    def add(self, url: str, title: str):
        """添加历史记录"""
        item = {
            'url': url,
            'title': title,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 插入到列表开头
        self._history.insert(0, item)
        
        # 限制数量
        if len(self._history) > self.max_items:
            self._history = self._history[:self.max_items]
        
        # 保存
        self._save()
    
    def get_all(self) -> List[Dict]:
        """获取所有历史记录"""
        return self._history.copy()
    
    def clear(self):
        """清空历史记录"""
        self._history.clear()
        self._save()
    
    def set_max_items(self, max_items: int):
        """设置最大历史记录数量"""
        self.max_items = max_items
        # 如果当前数量超过新的限制，截断
        if len(self._history) > max_items:
            self._history = self._history[:max_items]
            self._save()
