# v1.0
# created by HelloWorld05
# in 2024.06.26
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
#导入相应模块
class WebView(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)
    def createWindow(self, webWindowType):
        return main_demo.browser
class MainDemo(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Pybrowser')
        self.setWindowIcon(QIcon('icons/python.png'))
        self.resize(1024, 768)
        self.show()
        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏支持输入地址回车访问
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # 添加标签栏
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        # 允许关闭标签
        self.tabs.setTabsClosable(True)
        # 设置关闭按钮的槽
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.add_new_tab(QUrl('https://cn.bing.com/'), 'Bing搜索')
        self.setCentralWidget(self.tabs)
        new_tab_action = QAction(QIcon('icons/add_page.png'), 'New Page', self)
        new_tab_action.triggered.connect(self.add_new_tab)
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标大小
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        forward_button = QAction(QIcon('icons/forward.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/stop.png'), 'Stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'Reload', self)
        back_button.triggered.connect(self.tabs.currentWidget().back)
        forward_button.triggered.connect(self.tabs.currentWidget().forward)
        stop_button.triggered.connect(self.tabs.currentWidget().stop)
        reload_button.triggered.connect(self.tabs.currentWidget().reload)
        # 将按钮添加至导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(forward_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)
    # 响应回车按钮，将浏览器当前访问的URL设置为用户输入的URL
    def navigate_to_url(self):
        current_url = QUrl(self.urlbar.text())
        if current_url.scheme() == '':
            current_url.setScheme('http')
        self.tabs.currentWidget().load(current_url)
    # 将当前网页的链接更新到地址栏
    def renew_urlbar(self, url, browser=None):
        # 非当前窗口不更新URL
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)
    # 添加新的标签页
    def add_new_tab(self, qurl=QUrl(''), label='Blank'):
        # 设置浏览器
        self.browser = WebView(self)
        self.browser.load(qurl)
        # 为标签添加索引方便管理
        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.renew_urlbar(qurl, self.browser))
        # 将标签标题改为网页相关的标题
        self.browser.loadFinished.connect(
            lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))
    # 双击标签栏打开新页面
    def tab_open(self, i):
        if i == -1:
            self.add_new_tab()
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.renew_urlbar(qurl, self.tabs.currentWidget())
    def close_current_tab(self, i):
        # 若当前标签页只有一个则不关闭
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
if __name__ == '__main__':
    my_application = QApplication(sys.argv)  # 创建QApplication类的实例
    main_demo = MainDemo()
    main_demo.show()
    my_application.exec_()
