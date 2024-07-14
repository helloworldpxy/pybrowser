# v1.1
# created by HelloWorld05
# in 2024.06.19
# modified by RedstoneLu
# in 2024.07.14
#本次更新添加了多线程技术渲染，加载网页更流畅，更新了起始页

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
import subprocess

# 创建一个继承自QThread的类，用于在后台线程中加载网页
class RenderThread(QThread):
    # 初始化方法，接收要加载的URL
    def __init__(self, url, parent=None):
        super(RenderThread, self).__init__(parent)
        self.url = url
        self.page = QWebEnginePage()  # 创建一个网页对象

    # 线程启动时调用的方法
    def run(self):
        self.page.load(self.url)  # 在线程中加载网页
        self.page.loadFinished.connect(self.loadFinished)  # 当加载完成时，调用loadFinished方法

    # 网页加载完成后的槽函数
    def loadFinished(self, result):
        self.page.toHtml(self.htmlReady)  # 获取网页的HTML内容

    # 当网页的HTML内容准备就绪时的槽函数
    def htmlReady(self, html):
        self.html = html  # 存储HTML内容
        self.finished.emit()  # 发出完成信号

# 继承QWebEngineView的自定义WebView类
class WebView(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)
        self.render_thread = None  # 初始化渲染线程为None

    # 重写createWindow方法，用于新窗口的创建
    def createWindow(self, webWindowType):
        return main_window.browser

    # 加载URL的方法，使用新的线程来加载
    def loadUrl(self, url):
        self.render_thread = RenderThread(url)  # 创建渲染线程
        self.render_thread.finished.connect(self.renderFinished)  # 连接完成信号到槽函数
        self.render_thread.start()  # 启动线程

    # 当渲染线程完成时的槽函数
    def renderFinished(self):
        self.setHtml(self.render_thread.html)  # 设置网页内容
        self.render_thread.quit()  # 停止线程
        self.render_thread.wait()  # 等待线程结束
        self.render_thread = None  # 清理线程引用

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('LCbrowser')
        self.setWindowIcon(QIcon('icons/icon.png'))
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
         # 修改：默认加载本地HTML文件
        self.add_new_tab(QUrl("http://start.ltcld.com.cn/"), '首页')
        self.setCentralWidget(self.tabs)
        new_tab_action = QAction(QIcon('icons/add_page.png'), 'New Page', self)
        new_tab_action.triggered.connect(self.add_new_tab)
         # 修改：在用户打开浏览器时运行JavaScript代码
        self.browser.page().runJavaScript("cYear = 2024;")
        self.browser.loadFinished.connect(lambda _: self.browser.page().runJavaScript("cYear = 2024;"))
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标大小
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)
        # 添加前进、后退、停止加载和刷新的按钮
        self.add_navigation_buttons(navigation_bar)  # 修改：添加了add_navigation_buttons方法
        navigation_bar.addWidget(self.urlbar)

    def add_navigation_buttons(self, navigation_bar):  # 修改：新方法，减少代码重复
        buttons = [
            ('back', 'Back', self.tabs.currentWidget().back),
            ('forward', 'Forward', self.tabs.currentWidget().forward),
            ('stop', 'Stop', self.tabs.currentWidget().stop),
            ('reload', 'Reload', self.tabs.currentWidget().reload),
        ]
        for icon, text, slot in buttons:
            action = QAction(QIcon(f'icons/{icon}.png'), text, self)
            action.triggered.connect(slot)
            navigation_bar.addAction(action)

    # 响应回车按钮，将浏览器当前访问的URL设置为用户输入的URL
    def navigate_to_url(self):
        url_text = self.urlbar.text()
        # 修改：检查URL是否有效
        if not url_text.startswith(('http:', 'https:')):
            url_text = 'http://' + url_text
        current_url = QUrl(url_text)
        self.tabs.currentWidget().load(current_url)

    # 将当前网页的链接更新到地址栏
    def renew_urlbar(self, url, browser=None):
        # 非当前窗口不更新URL
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)

         # 添加新的标签页
    def add_new_tab(self, qurl=QUrl("http://start.ltcld.com.cn/"), label='NewTab'):
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
        if i != -1:  # 修改：添加了对索引的检查
            qurl = self.tabs.currentWidget().url()
            self.renew_urlbar(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):
        # 若当前标签页只有一个则不关闭
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 修改：将my_application改为更符合PEP 8的app
    main_window = MainWindow()  # 修改：将main_demo改为更描述性的main_window
    main_window.show()
    sys.exit(app.exec_())  # 修改：使用sys.exit来确保程序干净退出
