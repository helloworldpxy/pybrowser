# utils/bookmarks.py
# PyBrowser v2.5 - 书签管理

import json
from pathlib import Path
from typing import List, Dict


class BookmarkManager:
    """书签管理器，负责书签的持久化存储"""
    
    def __init__(self):
        self._bookmarks: List[Dict] = []
        self._config_dir = self._get_config_dir()
        self._bookmarks_file = self._config_dir / "bookmarks.json"
        
        # 确保配置目录存在
        self._config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载书签
        self._load()
    
    def _get_config_dir(self) -> Path:
        """获取配置目录"""
        home = Path.home()
        return home / ".pybrowser"
    
    def _load(self):
        """从文件加载书签"""
        try:
            if self._bookmarks_file.exists():
                with open(self._bookmarks_file, 'r', encoding='utf-8') as f:
                    self._bookmarks = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._bookmarks = []
    
    def _save(self):
        """保存书签到文件"""
        try:
            with open(self._bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(self._bookmarks, f, ensure_ascii=False, indent=2)
        except IOError:
            pass  # 静默处理写入错误
    
    def add(self, url: str, title: str):
        """添加书签"""
        from datetime import datetime
        
        bookmark = {
            'url': url,
            'title': title,
            'added': datetime.now().strftime("%Y-%m-%d")
        }
        
        # 检查是否已存在
        for existing in self._bookmarks:
            if existing['url'] == url:
                return False
        
        self._bookmarks.append(bookmark)
        self._save()
        return True
    
    def remove(self, index: int):
        """删除指定索引的书签"""
        if 0 <= index < len(self._bookmarks):
            self._bookmarks.pop(index)
            self._save()
            return True
        return False
    
    def remove_by_url(self, url: str):
        """删除指定 URL 的书签"""
        for i, bookmark in enumerate(self._bookmarks):
            if bookmark['url'] == url:
                self._bookmarks.pop(i)
                self._save()
                return True
        return False
    
    def get_all(self) -> List[Dict]:
        """获取所有书签"""
        return self._bookmarks.copy()
    
    def update(self, bookmarks: List[Dict]):
        """更新书签列表"""
        self._bookmarks = bookmarks.copy()
        self._save()
    
    def is_bookmarked(self, url: str) -> bool:
        """检查 URL 是否已添加书签"""
        return any(b['url'] == url for b in self._bookmarks)
