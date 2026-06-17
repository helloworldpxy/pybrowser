# core/web_view.py
# PyBrowser v2.5 - 自定义 WebView 组件

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon


class WebPage(QWebEnginePage):
    """自定义网页，处理新窗口请求等"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def createWindow(self, window_type):
        """在新标签页中打开链接，而不是新窗口"""
        # 通过父级的信号触发新标签页创建
        new_view = WebView()
        return new_view.page()


class WebView(QWebEngineView):
    """自定义 WebView 组件，扩展基础功能"""
    
    # 自定义信号
    title_changed = pyqtSignal(str)
    url_changed = pyqtSignal(QUrl)
    load_progress = pyqtSignal(int)
    load_finished = pyqtSignal(bool)
    icon_changed = pyqtSignal(QIcon)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置自定义页面
        self._page = WebPage(self)
        self.setPage(self._page)
        
        # 连接信号
        self.titleChanged.connect(self._on_title_changed)
        self.urlChanged.connect(self._on_url_changed)
        self.loadProgress.connect(self._on_load_progress)
        self.loadFinished.connect(self._on_load_finished)
        self.iconChanged.connect(self._on_icon_changed)
    
    def _on_title_changed(self, title: str):
        """标题变化处理"""
        self.title_changed.emit(title)
    
    def _on_url_changed(self, url: QUrl):
        """URL 变化处理"""
        self.url_changed.emit(url)
    
    def _on_load_progress(self, progress: int):
        """加载进度处理"""
        self.load_progress.emit(progress)
    
    def _on_load_finished(self, ok: bool):
        """加载完成处理"""
        self.load_finished.emit(ok)
    
    def _on_icon_changed(self, icon: QIcon):
        """图标变化处理"""
        self.icon_changed.emit(icon)
    
    def navigate_to(self, url: str):
        """导航到指定 URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.setUrl(QUrl(url))
    
    def get_url(self) -> str:
        """获取当前 URL"""
        return self.url().toString()
    
    def get_title(self) -> str:
        """获取当前标题"""
        return self.page().title()
