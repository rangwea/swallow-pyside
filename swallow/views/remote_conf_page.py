from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QHBoxLayout, QPushButton, QStackedWidget, QLineEdit, \
    QFormLayout, QMessageBox

from swallow.widgets import popup
from swallow.widgets.buttons import TitlebarButtons


class RemoteConfPage(QWidget):

    def __init__(self, parent):
        super(RemoteConfPage, self).__init__()
        self.parent = parent
        # 右侧内容区 > 配置页
        v = QVBoxLayout()
        v.setSpacing(0)
        v.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v)

        self.gitee_btn = QPushButton('gitee')
        self.gitee_btn.setCheckable(True)
        self.gitee_btn.setObjectName('header-tab-btn')
        self.github_btn = QPushButton('github')
        self.github_btn.setCheckable(True)
        self.github_btn.setObjectName('header-tab-btn')
        self.cos_btn = QPushButton('cos')
        self.cos_btn.setCheckable(True)
        self.cos_btn.setObjectName('header-tab-btn')

        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(True)
        self.btn_group.addButton(self.gitee_btn)
        self.btn_group.addButton(self.github_btn)
        self.btn_group.addButton(self.cos_btn)

        # header
        hw = QWidget()
        hw.setObjectName('page_header')
        v.addWidget(hw)
        header_ly = QHBoxLayout()
        hw.setLayout(header_ly)

        header_ly.addStretch(1)
        header_ly.addWidget(self.gitee_btn)
        header_ly.addWidget(self.github_btn)
        header_ly.addWidget(self.cos_btn)
        header_ly.addStretch(1)

        # 配置 Tab
        self.conf_widget = QStackedWidget(self)
        self.conf_widget.setObjectName('conf_page')
        self.conf_widget.addWidget(ConfWidget('gitee', self.parent, (
            ('repository', QLineEdit()), ('email', QLineEdit()), ('token', QLineEdit()), ('cname', QLineEdit()))))
        self.conf_widget.addWidget(ConfWidget('github', self.parent, (
            ('repository', QLineEdit()), ('email', QLineEdit()), ('token', QLineEdit()), ('cname', QLineEdit()))))
        self.conf_widget.addWidget(ConfWidget('cos', self.parent, (
            ('appId', QLineEdit()), ('secretId', QLineEdit()), ('secretKey', QLineEdit()), ('regionInfo', QLineEdit()),
            ('bucketName', QLineEdit()))))

        v.addWidget(self.conf_widget)
        # 初始显示
        self.gitee_btn.setChecked(True)
        self.__item_active(0)

        self.btn_group.buttonClicked.connect(self.__item_changed)

    def init_show(self):
        self.__item_active(0)

    def __item_changed(self, b:QPushButton):
        b.setFocus()
        i = self.btn_group.buttons().index(b)
        self.__item_active(i)

    def __item_active(self, i):
        self.conf_widget.setCurrentIndex(i)
        self.conf_widget.currentWidget().fill()


class ConfWidget(QWidget):
    def __init__(self, conf_name, parent, inputs):
        super(ConfWidget, self).__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setObjectName('conf_page')
        self.conf_name = conf_name
        self.parent = parent
        self.api = parent.api
        # views-model 关联
        self.view_model = {}
        self.inputs = inputs

        h = QHBoxLayout()
        self.form_layout = QFormLayout()
        for i in inputs:
            self._add_widget(i[0], i[1])
        
        h.addStretch(1)
        h.addLayout(self.form_layout)
        h.addStretch(1)

        self.save_button = QPushButton('保存')
        self.save_button.setObjectName('form_button')
        self.save_button.clicked.connect(self.save)

        self.form_layout.addWidget(self.save_button)

        self.setLayout(h)

    def _add_widget(self, field, widget: QWidget):
        self.form_layout.addRow(field, widget)
        self.view_model[widget] = field

    def fill(self):
        conf = self.api.conf_get(self.conf_name)
        if conf:
            for view, model in self.view_model.items():
                view.setText(conf.get(model))

    def save(self):
        # check null
        for i in self.inputs:
            i = i[1]
            if not i.text():
                popup.ins.warn('配置项不能为空')
                return

        conf = {model: view.text() for view, model in self.view_model.items()}
        try:
            self.api.conf_save(self.conf_name, conf)
            popup.ins.info('保存成功')
        except Exception as e:
            QMessageBox.warning(self.parent, 'error', f'保存失败：{e}')

