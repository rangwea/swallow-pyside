from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, \
    QMainWindow

from swallow.widgets import popup
from swallow.widgets.buttons import TitlebarButtons
from swallow.widgets.inputs import ImageInput


class SiteConfPage(QWidget):

    def __init__(self, parent: QMainWindow):
        super(SiteConfPage, self).__init__()
        self.parent = parent
        self.api = parent.api

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # header
        header_ly = QHBoxLayout()
        header_ly.addStretch(1)
        hw = QWidget()
        hw.setObjectName('page_header')
        hw.setLayout(header_ly)
        layout.addWidget(hw)

        conf = self.api.site_conf_get()

        form_h = QHBoxLayout()
        
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setContentsMargins(0, 0, 0, 0)

        self.q_title = QLineEdit()
        self.q_title.setText(conf['title'])
        self.form_layout.addRow('title', self.q_title)

        self.q_description = QLineEdit()
        self.q_description.setText(conf['description'])
        self.form_layout.addRow('description', self.q_description)

        self.q_theme = QComboBox()
        self.q_theme.addItems(['stack', 'jane', 'mini'])
        self.q_theme.setCurrentText(conf['theme'])
        self.form_layout.addRow('theme', self.q_theme)

        self.q_copyright = QLineEdit()
        self.q_copyright.setText(conf['copyright'])
        self.form_layout.addRow('copyright', self.q_copyright)

        self.q_author = QLineEdit()
        self.q_author.setText(conf['author']['name'])
        self.form_layout.addRow('author', self.q_author)

        self.save_button = QPushButton('保存')
        self.save_button.setObjectName('form_button')
        self.save_button.clicked.connect(self.save)
        self.form_layout.addWidget(self.save_button)

        form_h.addStretch(1)
        form_h.addLayout(self.form_layout)
        form_h.addStretch(1)

        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget(ImageInput('请选择 avatar 图片', self.api.hugos.static_img_path / 'avatar.png'))
        h.addWidget(ImageInput('请选择 favicon 图片', self.api.hugos.static_img_path / 'favicon.ico'))
        h.addStretch(1)

        v = QVBoxLayout()
        v.addSpacing(20)
        v.addLayout(form_h)
        v.addSpacing(50)
        v.addLayout(h)
        v.addStretch(1)

        layout.addLayout(v)

    def init_show(self):
        pass

    def save(self):
        conf = {
            'title': self.q_title.text(),
            'description': self.q_description.text(),
            'theme': self.q_theme.currentText(),
            'copyright': self.q_copyright.text(),
            'author': {
                'name': self.q_author.text()
            },
        }
        self.api.site_conf_save(conf)
        popup.ins.info('保存成功')
