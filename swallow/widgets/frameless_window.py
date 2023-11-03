import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow

try:
    if sys.platform == "darwin":
        import objc
except:
    pass


class FramelessWindow(QMainWindow):

    def __init__(self, draggable_objs):
        super(FramelessWindow, self).__init__()

        self._draggable_objs = draggable_objs
        self._draggable = False

        self._setup_titlebar()

    def _setup_titlebar(self):
        if sys.platform == "darwin":
            try:
                view = objc.objc_object(c_void_p=self.winId().__int__())
                __nsWindow = view.window()
                __nsWindow.setStyleMask_(__nsWindow.styleMask() | 1 << 15) # AppKit.NSFullSizeContentViewWindowMask = 1 << 15
                __nsWindow.setTitlebarAppearsTransparent_(True)
            except:
                pass

    # 鼠标移动事件
    def mouseMoveEvent(self, e):
        if self._draggable:
            self.window().windowHandle().startSystemMove()

    # 鼠标按下事件
    def mousePressEvent(self, a0:QMouseEvent):
        # 根据鼠标按下时的位置判断是否在可拖动对象范围内
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() in self._draggable_objs:
            self._draggable = True

    # 鼠标松开事件
    def mouseReleaseEvent(self, a0):
        self._draggable = False

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, a0):
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() in self._draggable_objs:
            if a0.button() == Qt.MouseButton.LeftButton:
                self.max_or_normal()

    # 切换最大化与正常大小
    def max_or_normal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()