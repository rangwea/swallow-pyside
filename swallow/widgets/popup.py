import time

from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QPoint, QObject, QEasingCurve
from PySide6.QtWidgets import QMainWindow, QPushButton, QGraphicsOpacityEffect


ins = None


class Popups(QObject):
    """
    popup message:
    process timeline: show a popup > timeout close > fade out first popup > float up other popup
    """
    __showings = []

    def __init__(self, win: QMainWindow,
                 timeout=1000,
                 info_color='rgb(0,139,69)',
                 warn_color='rgb(238,180,34)',
                 error_color='rgb(255,69,0)',
                 w=200,
                 h=24):
        super(Popups, self).__init__()
        self._win = win
        self.background_colors = {
            Popup.INFO: info_color,
            Popup.WARN: warn_color,
            Popup.ERROR: error_color,
        }
        self.popup_w = w
        self.popup_h = h

        self.timer = QTimer(self)
        self.timer.setInterval(timeout)
        self.timer.timeout.connect(self._timeout_close)

    def info(self, msg):
        """
        print info msg
        """
        self.print(Popup.INFO, msg)

    def warn(self, msg):
        """
        print warn msg
        """
        self.print(Popup.WARN, msg)

    def error(self, msg):
        """
        print error msg
        """
        self.print(Popup.ERROR, msg)

    def print(self, level, msg):
        """
        print msg
        """
        m = Popup(self._win, msg, len(self.__showings) + 1, self.background_colors[level], self.popup_w, self.popup_h)
        m.fadeout_finished.connect(self._fadeout_remove)
        self.__showings.append(m)
        m.show()
        if len(self.__showings) == 1:
            self.timer.start()

    def _timeout_close(self):
        """
        msg show time out
        """
        self.timer.stop()
        if self.__showings:
            m = self.__showings[0]
            m.start_fadeout()

    def _fadeout_remove(self):
        """
        When first popup has fade out, floating other popup and start next time interval
        :return:
        """
        if self.__showings:
            del self.__showings[0]
            for e in self.__showings:
                e.float_up()
            if self.__showings:
                self.timer.start()


class Popup(QPushButton):
    """
    popup element
    """
    INFO = 1
    WARN = 2
    ERROR = 3

    fadeout_finished = Signal()

    def __init__(self, win: QMainWindow,
                 msg,
                 index,
                 background_color,
                 w=200,
                 h=24):
        """
        :param win: QMainWindow
        :param msg: message
        :param index: index of current showing popup
        :param background_color:
        """
        super(Popup, self).__init__()
        self.id = time.time()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setText(msg)
        self.setFixedSize(w, h)
        self._move_y = h + 6
        self.move(win.x() + (win.width() - self.width()) / 2, win.y() - 20 + self._move_y * index)
        self._point = self.pos()

        stylesheet = f'''QPushButton {{
                font-size: 14px;
                border-radius: 12px;
                color: white;
                background-color: {background_color};
                }}'''
        self.setStyleSheet(stylesheet)

        oe = QGraphicsOpacityEffect(self)
        oe.setOpacity(1)
        self.setGraphicsEffect(oe)

        self.fadeout_ani = QPropertyAnimation(oe, b'opacity')
        self.fadeout_ani.setDuration(200)
        self.fadeout_ani.setStartValue(1)
        self.fadeout_ani.setEndValue(0)
        self.fadeout_ani.setEasingCurve(QEasingCurve.Type.Linear)
        self.fadeout_ani.finished.connect(self._on_fadeout_finished)

        self.float_ani = QPropertyAnimation(self, b'pos')
        self.float_ani.setDuration(400)
        self.float_ani.setEasingCurve(QEasingCurve.Type.OutBounce)

    def _on_fadeout_finished(self):
        self.fadeout_finished.emit()
        self.setParent(None)

    def float_up(self):
        """
        float to up
        """
        self.float_ani.setStartValue(self._point)
        self._point -= QPoint(0, self._move_y)
        self.float_ani.setEndValue(self._point)
        self.float_ani.start()

    def start_fadeout(self):
        """
        starting fade out animate
        """
        self.fadeout_ani.start()
