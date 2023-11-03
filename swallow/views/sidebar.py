from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QStackedWidget, \
    QLabel, QListWidget, QListWidgetItem, QFrame, QPushButton, QToolButton, QButtonGroup, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QPoint, Signal

from swallow.widgets import popup


def set_checked_icon(btn: QPushButton, icon, checked_icon):
    btn.setStyleSheet(f'''
            QPushButton {{ image: url({icon}); image-position: center left;}}
            :checked{{ image: url({checked_icon}); image-position: center left;}}
            ''')


class Sidebar(QWidget):
    item_changed = Signal(int)

    def __init__(self, parent, w=160):
        super(Sidebar, self).__init__()
        self.parent = parent
        self.api = parent.api
        self.setFixedWidth(w)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('sidebar')

        # logo
        self.logo = QLabel()
        self.logo.setFixedSize(80, 80)
        p = QPixmap(':logo.png')
        self.logo.setObjectName('logo')
        self.logo.setScaledContents(True)
        self.logo.setPixmap(p)

        self.group = QButtonGroup()
        self.group.setExclusive(True)

        # menu>歌曲
        self.article_menu_item = QPushButton(' ' * 8 + '文章')
        self.article_menu_item.setObjectName('menu-item')
        self.article_menu_item.setCheckable(True)
        self.article_menu_item.setChecked(True)
        set_checked_icon(self.article_menu_item, ':article.svg', ':article-white.svg')
        self.group.addButton(self.article_menu_item)
        # menu>专辑
        self.conf_menu_item = QPushButton(' ' * 8 + '配置')
        self.conf_menu_item.setObjectName('menu-item')
        self.conf_menu_item.setCheckable(True)
        set_checked_icon(self.conf_menu_item, ':setting.svg', ':setting-white.svg')
        self.group.addButton(self.conf_menu_item)
        # menu>艺人
        self.remote_menu_item = QPushButton(' ' * 8 + '远程')
        self.remote_menu_item.setObjectName('menu-item')
        self.remote_menu_item.setCheckable(True)
        set_checked_icon(self.remote_menu_item, ':deploy.svg', ':deploy-white.svg')
        self.group.addButton(self.remote_menu_item)

        # 左侧 sidebar -> button
        self.preview_btn = QPushButton(" 预览")
        self.preview_btn.setObjectName('sidebar_button')
        self.preview_btn.setIcon(QIcon(':preview.svg'))
        self.preview_btn.clicked.connect(self.api.site_preview)
        self.deploy_btn = QPushButton(" 部署")
        self.deploy_btn.setObjectName('sidebar_button')
        self.deploy_btn.setIcon(QIcon(':deploy.svg'))
        self.deploy_btn.clicked.connect(self.site_deploy)
        self.app_info_label = QLabel('swallow v1.0.0')
        self.app_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignHCenter)

        # 布局
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.article_menu_item)
        self.layout.addWidget(self.conf_menu_item)
        self.layout.addWidget(self.remote_menu_item)
        self.layout.addStretch(1)
        self.layout.addWidget(self.preview_btn)
        self.layout.addSpacing(7)
        self.layout.addWidget(self.deploy_btn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.app_info_label)

        self.setLayout(self.layout)

        self.group.buttonClicked.connect(self.__item_changed)

    def __item_changed(self, b: QPushButton):
        b.setFocus()
        i = self.group.buttons().index(b)
        self.item_changed.emit(i)

    def site_deploy(self):
        try:
            self.deploy_btn.setDisabled(True)
            self.api.site_deploy()
            popup.ins.info('部署成功')
            self.deploy_btn.setDisabled(False)
        except Exception as e:
            self.deploy_btn.setDisabled(False)
            QMessageBox.warning(self.parent, 'swallow', f'部署失败：{e}')
