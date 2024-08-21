# v1.1.0 Beta3
# created by HelloWorld05
# in 2024.06.19
# modified by RedstoneLu
# in 2024.8.21
# 修复了标签页的问题，祝开发团队的郭师傅生日快乐！！
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class RenderThread(QThread):
    finished = pyqtSignal()

    def __init__(self, url, parent=None):
        super(RenderThread, self).__init__(parent)
        self.url = url
        self.html = None

    def run(self):
        # Placeholder for the web page loading simulation
        pass  # Actual code should load QWebEnginePage and handle loading

class WebView(QWebEngineView):
    url_changed = pyqtSignal(QUrl)
    title_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        self.loadFinished.connect(self.on_load_finished)
        self.urlChanged.connect(self.on_url_changed)

    def loadUrl(self, url):
        self.load(QUrl(url))
        self.url_changed.emit(self.url())

    def on_load_finished(self):
        self.title_changed.emit(self.title())

    def on_url_changed(self, qurl):
        # Emit the URL changed signal with the current URL
        self.url_changed.emit(qurl)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('LCbrowser')
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.resize(1024, 768)

        self.browser = WebView(self)
        self.browser.loadUrl("https://start.ltcld.com.cn/")
        self.browser.url_changed.connect(self.update_urlbar)
        self.browser.title_changed.connect(self.update_tab_title)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.addTab(self.browser, '首页')

        self.setCentralWidget(self.tabs)

        self.urlbar = QLineEdit(self)
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.navigation_bar = QToolBar('Navigation')
        self.navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(self.navigation_bar)
        self.add_navigation_buttons(self.navigation_bar)
        self.navigation_bar.addWidget(self.urlbar)

        self.add_toolbar_actions(self.navigation_bar)

    def add_navigation_buttons(self, navigation_bar):
        back_action = QAction(QIcon('icons/back.png'), 'Back', self)
        back_action.triggered.connect(lambda: self.tabs.currentWidget().back() if self.tabs.currentWidget() else None)
        navigation_bar.addAction(back_action)

        forward_action = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward_action.triggered.connect(lambda: self.tabs.currentWidget().forward() if self.tabs.currentWidget() else None)
        navigation_bar.addAction(forward_action)

        stop_action = QAction(QIcon('icons/stop.png'), 'Stop', self)
        stop_action.triggered.connect(lambda: self.tabs.currentWidget().stop() if self.tabs.currentWidget() else None)
        navigation_bar.addAction(stop_action)

    def add_toolbar_actions(self, navigation_bar):
        add_page_action = QAction(QIcon('icons/add_page.png'), 'Add Page', self)
        add_page_action.triggered.connect(self.add_new_tab)
        navigation_bar.addAction(add_page_action)

        return_home_action = QAction(QIcon('icons/home.png'), 'Home', self)
        return_home_action.triggered.connect(self.return_home)
        navigation_bar.addAction(return_home_action)

        refresh_action = QAction(QIcon('icons/refresh.png'), 'Refresh', self)
        refresh_action.triggered.connect(self.refresh_page)
        navigation_bar.addAction(refresh_action)

        about_action = QAction(QIcon('icons/about.png'), 'About', self)
        about_action.triggered.connect(self.show_about)
        navigation_bar.addAction(about_action)

    def navigate_to_url(self):
        url_text = self.urlbar.text()
        if not url_text.startswith(('http:', 'https:')):
            url_text = 'http://' + url_text
        current_url = QUrl(url_text)
        self.browser.loadUrl(current_url)

    def update_urlbar(self, url):
        # Update the URL bar to display the current URL of the WebView
        self.urlbar.setText(url.toString())

    def update_tab_title(self, title):
        current_index = self.tabs.currentIndex()
        self.tabs.setTabText(current_index, title)

    def add_new_tab(self):
        new_browser = WebView(self)
        new_browser.loadUrl("https://start.ltcld.com.cn/")
        new_browser.url_changed.connect(self.update_urlbar)
        new_browser.title_changed.connect(self.update_tab_title)
        self.tabs.addTab(new_browser, 'New Tab')
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def close_current_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)

    def refresh_page(self):
        self.browser.reload()

    def return_home(self):
        self.browser.loadUrl("https://start.ltcld.com.cn/")

    def show_about(self):
        QMessageBox.about(self, '关于 LCbrowser',
                          '版本号: 1.1.0 Beta3\n'
                          '这是一个基于PyQt5和QWebEngineWidgets开发的简洁网络浏览器\n'
                          'QQ交流群：967746037')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())