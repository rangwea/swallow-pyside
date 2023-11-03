# coding:utf-8
from enum import Enum

from PySide6.QtCore import Qt, Property, QFile, QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QAbstractButton, QWidget, QHBoxLayout
from PySide6.QtXml import QDomDocument


class State(Enum):
    """ Title bar button state """
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class CustomButton(QAbstractButton):
    """ Title bar button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCursor(Qt.ArrowCursor)
        self.setFixedSize(22, 22)
        self._state = State.NORMAL

        # icon color
        self._normalColor = QColor(100, 110, 110)
        self._hoverColor = QColor(255, 255, 255)
        self._pressedColor = QColor(255, 255, 255)

        # background color
        self._normalBgColor = QColor(0, 0, 0, 0)
        self._hoverBgColor = QColor(0, 0, 0, 26)
        self._pressedBgColor = QColor(0, 0, 0, 51)

    def setState(self, state):
        """ set the state of button

        Parameters
        ----------
        state: State
            the state of button
        """
        self._state = state
        self.update()

    def isPressed(self):
        """ whether the button is pressed """
        return self._state == State.PRESSED

    def getNormalColor(self):
        """ get the icon color of the button in normal state """
        return self._normalColor

    def getHoverColor(self):
        """ get the icon color of the button in hover state """
        return self._hoverColor

    def getPressedColor(self):
        """ get the icon color of the button in pressed state """
        return self._pressedColor

    def getNormalBackgroundColor(self):
        """ get the background color of the button in normal state """
        return self._normalBgColor

    def getHoverBackgroundColor(self):
        """ get the background color of the button in hover state """
        return self._hoverBgColor

    def getPressedBackgroundColor(self):
        """ get the background color of the button in pressed state """
        return self._pressedBgColor

    def setNormalColor(self, color):
        """ set the icon color of the button in normal state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._normalColor = QColor(color)
        self.update()

    def setHoverColor(self, color):
        """ set the icon color of the button in hover state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._hoverColor = QColor(color)
        self.update()

    def setPressedColor(self, color):
        """ set the icon color of the button in pressed state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._pressedColor = QColor(color)
        self.update()

    def setNormalBackgroundColor(self, color):
        """ set the background color of the button in normal state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._normalBgColor = QColor(color)
        self.update()

    def setHoverBackgroundColor(self, color):
        """ set the background color of the button in hover state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._hoverBgColor = QColor(color)
        self.update()

    def setPressedBackgroundColor(self, color):
        """ set the background color of the button in pressed state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._pressedBgColor = QColor(color)
        self.update()

    def enterEvent(self, e):
        self.setState(State.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState(State.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        self.setState(State.PRESSED)
        super().mousePressEvent(e)

    def _getColors(self):
        """ get the icon color and background color """
        if self._state == State.NORMAL:
            return self._normalColor, self._normalBgColor
        elif self._state == State.HOVER:
            return self._hoverColor, self._hoverBgColor

        return self._pressedColor, self._pressedBgColor

    normalColor = Property(QColor, getNormalColor, setNormalColor)
    hoverColor = Property(QColor, getHoverColor, setHoverColor)
    pressedColor = Property(QColor, getPressedColor, setPressedColor)
    normalBackgroundColor = Property(QColor, getNormalBackgroundColor, setNormalBackgroundColor)
    hoverBackgroundColor = Property(QColor, getHoverBackgroundColor, setHoverBackgroundColor)
    pressedBackgroundColor = Property(QColor, getPressedBackgroundColor, setPressedBackgroundColor)


class SvgButton(CustomButton):
    """ Title bar button using svg icon """

    def __init__(self, parent, iconPath):
        """
        Parameters
        ----------
        iconPath: str
            the path of icon

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self._normal_svg_dom = QDomDocument()
        self._hover_svg_dom = QDomDocument()
        self._pressed_svg_dom = QDomDocument()

        self._has_fill_normal_svg = False
        self._has_fill_hover_svg = False
        self._has_fill_pressed_svg = False
        self.setIcon(iconPath)

    def setIcon(self, iconPath):
        """ set the icon of button

        Parameters
        ----------
        iconPath: str
            the path of icon
        """
        f = QFile(iconPath)
        f.open(QFile.ReadOnly)
        c = f.readAll()
        self._normal_svg_dom.setContent(c)
        self._hover_svg_dom.setContent(c)
        self._pressed_svg_dom.setContent(c)
        f.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        svgDom, bgColor = self._getSvgDomAndBgColor()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        renderer = QSvgRenderer(svgDom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))

    def _getSvgDomAndBgColor(self):
        """ get the icon color and background color """
        if self._state == State.NORMAL:
            return self._fillSvgDom(self._has_fill_normal_svg, self._normal_svg_dom,
                                    self._normalColor), self._normalBgColor
        elif self._state == State.HOVER:
            return self._fillSvgDom(self._has_fill_hover_svg, self._hover_svg_dom, self._hoverColor), self._hoverBgColor

        return self._fillSvgDom(self._has_fill_pressed_svg, self._pressed_svg_dom,
                                self._pressedColor), self._pressedBgColor

    def _fillSvgDom(self, has, dom, color):
        if not has:
            pathNodes = dom.elementsByTagName('path')
            for i in range(pathNodes.length()):
                element = pathNodes.at(i).toElement()
                element.setAttribute('stroke', color.name())
        return dom


class TitlebarButtons(QWidget):
    def __init__(self, parent=None):
        super(TitlebarButtons, self).__init__(parent)
        self.min_btn = MinimizeButton()
        self.max_btn = MaximizeButton()
        self.close_btn = CloseButton()
        self.setContentsMargins(0, 0, 0, 0)
        h = QHBoxLayout()
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self.min_btn)
        h.addWidget(self.max_btn)
        h.addWidget(self.close_btn)
        self.setFixedSize(self.min_btn.width() * 3 + 24, self.min_btn.height())
        self.setLayout(h)


class MinimizeButton(CustomButton):
    """ Minimize button """

    def __init__(self):
        super(MinimizeButton, self).__init__()

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 2)
        pen.setCosmetic(True)
        painter.setPen(pen)
        left_x = int((self.width() - 8) / 2)
        right_x = int(self.width() / 2 + 4)
        y = int(self.height() / 2)
        painter.drawLine(left_x, y, right_x, y)

    def mousePressEvent(self, e):
        self.window().showMinimized()
        super().mousePressEvent(e)


class MaximizeButton(CustomButton):
    """ Maximize button """

    def __init__(self):
        super().__init__()
        self._isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self._isMax == isMax:
            return

        self._isMax = isMax
        self.setState(State.NORMAL)

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        if self.window().isMaximized():
            self.window().showNormal()
            self.setMaxState(False)
        else:
            self.window().showMaximized()
            self.setMaxState(True)

        super().mousePressEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 2)
        pen.setCosmetic(True)
        painter.setPen(pen)

        w = self.width()
        h = self.height()
        rect_side = 8
        left_x = int((w - rect_side) / 2)
        top_y = int((h - rect_side) / 2)
        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self._isMax:
            painter.drawRect(int(left_x * r), int(top_y * r), int(8 * r), int(8 * r))
        else:
            painter.drawRect(int(left_x * r), int((top_y + 2) * r), int(6 * r), int(6 * r))
            x0 = int(left_x * r) + int(2 * r)
            y0 = top_y * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
            path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.drawPath(path)


class CloseButton(CustomButton):
    """ Close button """

    def __init__(self):
        super(CloseButton, self).__init__()
        self.setHoverBackgroundColor(QColor(232, 17, 35))
        self.setPressedBackgroundColor(QColor(241, 112, 122))

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 2)
        pen.setCosmetic(True)
        painter.setPen(pen)
        w = self.width()
        h = self.height()

        rect_side = 8
        left_x = int((w - rect_side) / 2)
        right_x = int((w - rect_side) / 2 + rect_side)
        top_y = int((h - rect_side) / 2)
        bottom_y = int((h - rect_side) / 2 + rect_side)
        painter.drawLine(left_x, top_y, right_x, bottom_y)
        painter.drawLine(right_x, top_y, left_x, bottom_y)

    def mousePressEvent(self, e):
        self.window().close()
