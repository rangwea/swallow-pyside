import shutil
from pathlib import Path
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog


class ImageInput(QWidget):
    def __init__(self, text, path: Path):
        super(ImageInput, self).__init__()
        self.path = path
        self.text = text
        v = QVBoxLayout()
        self.text_label = QLabel()
        self.text_label.setText(self.text)
        v.addWidget(self.text_label)

        self.img_label = QLabel()
        self.img_label.setToolTip(self.text)
        self.img_label.setFixedSize(120, 120)
        self.img_label.setScaledContents(True)
        self.img_label.setStyleSheet('border: 2px dashed rgb(220,220,220)')
        v.addWidget(self.img_label)
        self._show_img()
        self.setLayout(v)

    def _show_img(self):
        if self.path.exists():
            self.img_label.setPixmap(QPixmap(str(self.path)))

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            d = QFileDialog(self)
            d.setNameFilter('Images (*.png *.gif *.jpg)')
            d.exec()
            if d.selectedUrls():
                source = d.selectedUrls()[0].path()
                if source.endswith(('.png', '.jpg', '.gif')):
                    src_path = d.selectedUrls()[0].path()
                    if sys.platform == "win32":
                        src_path = src_path[1:]
                    shutil.copy(src_path, self.path)
                    self._show_img()