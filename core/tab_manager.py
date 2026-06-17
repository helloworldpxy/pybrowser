# core/tab_manager.py
# PyBrowser v2.5 - 标签页管理器

from PyQt5.QtCore import QUrl, pyqtSignal, QObject
from PyQt5.QtWidgets import QTabWidget

from .web_view import WebView


class TabManager(QObject):
    """标签页管理器，统一管理所有标签页的创建、关闭和切换"""
    
    # 自定义信号
    tab_created = pyqtSignal(int, WebView)
    tab_closed = pyqtSignal(int)
    current_changed = pyqtSignal(int)
    title_updated = pyqtSignal(int, str)
    url_updated = pyqtSignal(int, QUrl)
    load_progress_updated = pyqtSignal(int, int)
    
    def __init__(self, tab_widget: QTabWidget, parent=None):
        super().__init__(parent)
        self.tab_widget = tab_widget
        self._views: list[WebView] = []
        
        # 连接标签页信号
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self.tab_widget.currentChanged.connect(self._on_current_changed)
    
    def add_tab(self, url: QUrl = None, title: str = "新标签页") -> WebView:
        """添加新标签页"""
        if url is None:
            url = QUrl("https://www.google.com")
        
        view = WebView()
        view.setUrl(url)
        
        # 连接信号
        view.title_changed.connect(lambda t, v=view: self._on_view_title_changed(v, t))
        view.url_changed.connect(lambda u, v=view: self._on_view_url_changed(v, u))
        view.load_progress.connect(lambda p, v=view: self._on_view_load_progress(v, p))
        
        # 添加到标签页
        index = self.tab_widget.addTab(view, title)
        self._views.append(view)
        self.tab_widget.setCurrentIndex(index)
        
        self.tab_created.emit(index, view)
        return view
    
    def close_tab(self, index: int):
        """关闭指定标签页"""
        if self.tab_widget.count() > 1 and 0 <= index < len(self._views):
            view = self._views.pop(index)
            self.tab_widget.removeTab(index)
            view.deleteLater()
            self.tab_closed.emit(index)
    
    def current_view(self) -> WebView:
        """获取当前标签页的 WebView"""
        current_index = self.tab_widget.currentIndex()
        if 0 <= current_index < len(self._views):
            return self._views[current_index]
        return None
    
    def current_index(self) -> int:
        """获取当前标签页索引"""
        return self.tab_widget.currentIndex()
    
    def count(self) -> int:
        """获取标签页数量"""
        return self.tab_widget.count()
    
    def _on_tab_close_requested(self, index: int):
        """标签页关闭请求处理"""
        self.close_tab(index)
    
    def _on_current_changed(self, index: int):
        """当前标签页变化处理"""
        self.current_changed.emit(index)
    
    def _on_view_title_changed(self, view: WebView, title: str):
        """WebView 标题变化处理"""
        if view in self._views:
            index = self._views.index(view)
            # 限制标题长度
            display_title = title[:20] + "..." if len(title) > 20 else title
            self.tab_widget.setTabText(index, display_title)
            self.title_updated.emit(index, title)
    
    def _on_view_url_changed(self, view: WebView, url: QUrl):
        """WebView URL 变化处理"""
        if view in self._views:
            index = self._views.index(view)
            self.url_updated.emit(index, url)
    
    def _on_view_load_progress(self, view: WebView, progress: int):
        """WebView 加载进度处理"""
        if view in self._views:
            index = self._views.index(view)
            self.load_progress_updated.emit(index, progress)
