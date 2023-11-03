from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout, QWidget, QStackedWidget

from swallow.service import Api
from swallow.views.article_page import ArticlePage
from swallow.views.remote_conf_page import RemoteConfPage
from swallow.views.sidebar import Sidebar
from swallow.views.site_conf_page import SiteConfPage
from swallow.widgets import popup
from swallow.widgets.buttons import MinimizeButton, MaximizeButton, CloseButton, TitlebarButtons
from swallow.widgets.frameless_window import FramelessWindow
from swallow import resource
from swallow.widgets.popup import Popups


class MainWindow(FramelessWindow):

    def __init__(self, api: Api):
        super(MainWindow, self).__init__(['page_header', 'logo'])
        # set window ui
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1200, 800)

        self._startPos = None
        self._endPos = None
        self._isTracking = None

        self.api = api  # service api

        # 左侧 sidebar
        self.sidebar = Sidebar(self)

        # 右侧内容区
        self.right_widget = QStackedWidget(self)
        self.right_widget.setObjectName('sidebar_right')

        # 右侧内容区 > 文章列表页
        self.article_page = ArticlePage(self)
        self.right_widget.addWidget(self.article_page)

        # 右侧内容区 > 网站配置
        self.right_widget.addWidget(SiteConfPage(self))

        # 右侧内容区 >  配置页
        self.right_widget.addWidget(RemoteConfPage(self))

        # 默认显示第一个
        self.side_bar_changed(0)

        # 主布局 > 左侧 sidebar 和 右侧 page
        self.main_ly = QHBoxLayout()
        self.main_ly.setSpacing(0)
        self.main_ly.setContentsMargins(0, 0, 0, 0)
        self.main_ly.addWidget(self.sidebar)
        self.main_ly.addWidget(self.right_widget)
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main")
        self.main_widget.setLayout(self.main_ly)

        # 主布局 > 功能区和编辑器切换
        self.main_or_edit = QStackedWidget(self)
        self.main_or_edit.setObjectName('mainWidget')
        self.main_or_edit.addWidget(self.main_widget)
        self.main_or_edit.addWidget(self.article_page.markdown_editor)

        # 设置窗口主控件
        self.setCentralWidget(self.main_or_edit)

        # 设置控件事件
        self.sidebar.item_changed.connect(self.side_bar_changed)  # 左侧菜单选择
        self.article_page.list_or_editor_changed.connect(self.main_or_edit.setCurrentIndex)

        # 全局对象
        popup.ins = Popups(self)

    def side_bar_changed(self, i):
        self.right_widget.setCurrentIndex(i)
        self.right_widget.currentWidget().init_show()
