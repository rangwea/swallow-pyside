import shutil
import time
from pathlib import Path

import markdown
from PySide6.QtCore import Qt, QMimeData, QUrl, Signal
from PySide6.QtGui import QIcon, QTextTable, QTextTableFormat
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QCheckBox, \
    QLabel, QTextEdit, QFileDialog, QStackedWidget, QMessageBox, QLineEdit

from swallow.heighlight import MarkdownHighlighter
from swallow.models import Article
from swallow.style import PREVIEW_STYLE
from swallow.widgets.buttons import TitlebarButtons

ARTICLE_INIT_META = '''```
title = ""
tags = ["",""]
categories = [""]
description = ""
date = "{}"
```'''


def gen_aid():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())


class ArticlePage(QWidget):
    list_or_editor_changed = Signal(int)

    def __init__(self, parent):
        super(ArticlePage, self).__init__()
        self.parent = parent
        self.api = parent.api

        # 按钮>删除
        self.delete_btn = QPushButton(self)
        self.delete_btn.setObjectName('delete_icon_btn')
        self.delete_btn.setIcon(QIcon(':delete.svg'))
        p = self.delete_btn.sizePolicy()
        p.setRetainSizeWhenHidden(True)
        self.delete_btn.setSizePolicy(p)
        self.delete_btn.hide()
        # 控件>搜索
        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setPlaceholderText('支持通过标题、标签搜索')
        self.search_input.setObjectName('search-btn')
        self.search_input.setFixedSize(220, 25)
        self.search_input.addAction(QIcon(':search.svg'), QLineEdit.ActionPosition.LeadingPosition)
        # 控件>新建
        self.new_btn = QPushButton()
        self.new_btn.setObjectName('icon_btn')
        self.new_btn.setIcon(QIcon(':add.svg'))
        # 控件>列表
        self.article_list_widget = ArticleListWidget()
        self.article_list_widget.setObjectName('article_list')
        # 控件>编辑器
        self.markdown_editor = MarkdownEditor(parent, self.api.hugos.images_path.absolute())
        self.markdown_editor.connectQuit(self.article_edit_quit)
        self.markdown_editor.connectSave(self.article_save)

        # 布局
        v = QVBoxLayout()
        v.setSpacing(0)
        v.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v)
        # header
        header_ly = QHBoxLayout()
        header_ly.addWidget(self.delete_btn, stretch=1, alignment=Qt.AlignmentFlag.AlignLeft)
        header_ly.addWidget(self.search_input, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_ly.addWidget(self.new_btn, stretch=1, alignment=Qt.AlignmentFlag.AlignRight)

        hw = QWidget()
        hw.setObjectName('page_header')
        hw.setLayout(header_ly)
        v.addWidget(hw)
        # 文章列表
        v.addWidget(self.article_list_widget)

        self.search_input.returnPressed.connect(self.article_search)
        self.new_btn.clicked.connect(self.article_new)
        self.delete_btn.clicked.connect(self.article_delete)
        self.article_list_widget.itemClicked.connect(self.article_edit_show)  # 点击文章
        self.article_list_widget.item_check_changed.connect(self.article_item_check)

    def article_edit_show(self, item):
        item_w = self.article_list_widget.itemWidget(item)  # type: ArticleItem
        a = self.api.article_get(item_w.aid)
        self.markdown_editor.set_article(item_w.aid, a)
        self.list_or_editor_changed.emit(1)

    def article_edit_quit(self):
        self.list_or_editor_changed.emit(0)
        self.init_show()

    def init_show(self, search=None):
        """
        文章列表页
        :return:
        """
        self.article_list_widget.clear()
        self.article_list_widget.append(Article('about', '关于我'), checkable=False)
        articles = self.api.article_list(search)
        for a in articles:
            self.article_list_widget.append(a)
        self.article_list_widget.clear_selected()
        self.article_item_check()

    def article_save(self, text):
        self.api.article_save(self.markdown_editor.current_aid, text)

    def article_search(self):
        self.init_show(self.search_input.text())

    def article_new(self):
        self.markdown_editor.set_article(gen_aid(),
                                         ARTICLE_INIT_META.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.list_or_editor_changed.emit(1)

    def article_item_check(self):
        selected_size = len(self.article_list_widget.selected_aids)
        if selected_size:
            self.delete_btn.setText(f'已选择 {selected_size}')
            self.delete_btn.show()
        else:
            self.delete_btn.hide()

    def article_delete(self):
        selected = self.article_list_widget.selected_aids
        if selected:
            for s in selected:
                self.api.article_del(s)
        self.article_list_widget.selected_aids = []
        self.article_item_check()
        self.init_show()


class ArticleListWidget(QListWidget):
    item_check_changed = Signal()

    def __init__(self):
        super(ArticleListWidget, self).__init__()
        self.selected_aids = []

    def append(self, article: Article, checkable=True):
        w = QListWidgetItem(self)
        self.addItem(w)
        i = ArticleItem(article, self, checkable)
        i.check_changed.connect(self.__item_check_changed)
        self.setItemWidget(w, i)

    def __item_check_changed(self, state, aid):
        if state == 0:
            # uncheck
            self.selected_aids.remove(aid)
        elif state == 2:
            # check
            self.selected_aids.append(aid)

        self.item_check_changed.emit()

    def clear_selected(self):
        self.selected_aids = []


class ArticleItem(QWidget):
    check_changed = Signal(int, str)

    def __init__(self, article: Article, parent: ArticleListWidget, checkable=True):
        super(ArticleItem, self).__init__()
        self.parent = parent
        self.aid = article.aid
        layout = QHBoxLayout()
        if checkable:
            q = QCheckBox(article.title, self)
            q.stateChanged.connect(self.__checked)  # 选择
            q.setStyleSheet("QCheckBox {font-size: 18px;spacing: 12}")
            layout.addWidget(q, stretch=3)
        else:
            layout.addWidget(QLabel(article.title), stretch=3)
        layout.addWidget(QLabel(article.tags), stretch=1)
        layout.addWidget(QLabel(article.create_time), stretch=1)
        self.setLayout(layout)

    def __checked(self, state):
        self.check_changed.emit(state, str(self.aid))


class MarkdownEditor(QWidget):

    def __init__(self, parent, img_dir):
        super(MarkdownEditor, self).__init__()
        self.parent = parent
        self._changed = False
        self._quit_callback = None
        self._save_callback = None
        self._preview_state = 0  # 0 source 1 preview

        self.img_dir = img_dir
        self.current_aid = None

        self._preview_icon = QIcon(':preview.svg')
        self._source_icon = QIcon(':source.svg')

        self.save_notdone_icon = QIcon(':done-green.svg')
        self.save_done_icon = QIcon(':done.svg')

        v = QVBoxLayout()
        v.setSpacing(0)
        v.setContentsMargins(0, 0, 0, 0)

        self.quit_btn = QPushButton()
        self.quit_btn.setObjectName('icon_btn')
        self.quit_btn.setIcon(QIcon(':left.svg'))
        self.quit_btn.clicked.connect(self._quit)
        self.save_btn = QPushButton()
        self.save_btn.setObjectName('icon_btn')
        self.save_btn.setIcon(self.save_done_icon)
        self.save_btn.clicked.connect(self._save)

        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget(self.quit_btn)
        h.addWidget(self.save_btn)

        hw = QWidget()
        hw.setObjectName('page_header')
        hw.setLayout(h)
        v.addWidget(hw)

        tool_ly = QVBoxLayout()
        tool_ly.setContentsMargins(5, 0, 0, 0)
        tool_ly.setSpacing(10)
        self.preview_btn = QPushButton()
        self.preview_btn.setObjectName('icon_btn')
        self.preview_btn.setIcon(self._preview_icon)
        self.preview_btn.clicked.connect(self._preview_change)
        image_btn = QPushButton()
        image_btn.setObjectName('icon_btn')
        image_btn.setIcon(QIcon(':image.svg'))
        image_btn.clicked.connect(self._insert_images)
        tool_ly.addStretch(1)
        tool_ly.addWidget(self.preview_btn)
        tool_ly.addWidget(image_btn)
        tool_ly.addStretch(1)

        self.edit = MarkdownQTextEdit(self, img_dir)
        self.edit.setFixedWidth(800)
        self.edit.setObjectName('edit')
        self.edit.textChanged.connect(self._onchanged)
        MarkdownHighlighter(self.edit)

        self.preview = QTextEdit(self)
        self.preview.setFixedWidth(800)
        self.preview.setReadOnly(True)
        self.preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preview.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.edit_or_view_stack = QStackedWidget()
        self.edit_or_view_stack.addWidget(self.edit)
        self.edit_or_view_stack.addWidget(self.preview)

        tool_edit_ly = QHBoxLayout()
        tool_edit_ly.addLayout(tool_ly)
        tool_edit_ly.addStretch(1)
        tool_edit_ly.addWidget(self.edit_or_view_stack)
        tool_edit_ly.addStretch(1)

        v.addLayout(tool_edit_ly)

        self.setLayout(v)

    def _onchanged(self):
        self._changed = True
        self.save_btn.setIcon(self.save_notdone_icon)

    def _quit(self):
        if self._changed:
            m = QMessageBox()
            m.setText('文档被修改了')
            m.setInformativeText('请确认是否保存')
            m.setStandardButtons(
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Save)
            r = m.exec()
            if r == QMessageBox.StandardButton.Save:
                self._save()
                self._quit_callback()
            elif r == QMessageBox.StandardButton.Cancel:
                pass
            elif r == QMessageBox.StandardButton.Discard:
                self._quit_callback()
        else:
            self._quit_callback()
        self.edit.setText('')
        self._source()

    def _save(self):
        self._save_callback(self.edit.toPlainText())
        self._changed = False
        self.save_btn.setIcon(self.save_done_icon)

    def _preview_change(self):
        if self._preview_state:
            self._source()
        else:
            self._preview()

    def _preview(self):
        html = markdown.markdown(self.edit.toPlainText(), extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.tables',
        ])
        html = html.replace('<img ', '<img width="760" ')
        self.preview.setHtml(PREVIEW_STYLE + html)
        self.preview.document().setBaseUrl(QUrl(f'file:////{self.img_dir}/{self.current_aid}/'))
        for f in self.preview.document().rootFrame().childFrames():
            if type(f) == QTextTable:
                q = QTextTableFormat()
                q.setCellSpacing(0)
                q.setBorder(1)
                q.setWidth(800)
                q.setBorderCollapse(True)
                q.setTopMargin(10)
                q.setBottomMargin(10)
                f.setFormat(q)

        self._preview_state = 1
        self.preview_btn.setIcon(self._source_icon)
        self.edit_or_view_stack.setCurrentIndex(1)

    def _source(self):
        self._preview_state = 0
        self.preview_btn.setIcon(self._preview_icon)
        self.edit_or_view_stack.setCurrentIndex(0)

    def _insert_images(self):
        dialog = QFileDialog(self)
        dialog.setMimeTypeFilters(['png', 'jpg', 'jpeg', 'gif'])
        dialog.exec()
        files = dialog.selectedFiles()
        for f in files:
            i = Path(f)
            if i.is_file():
                self.edit.insert_image(i)

    def set_article(self, aid, text):
        self.current_aid = aid
        self.edit.setText(text)
        self._changed = False
        self.save_btn.setIcon(self.save_done_icon)

    def connectQuit(self, callback):
        self._quit_callback = callback

    def connectSave(self, callback):
        self._save_callback = callback


class MarkdownQTextEdit(QTextEdit):
    def __init__(self, parent: MarkdownEditor, img_dir):
        super(MarkdownQTextEdit, self).__init__()
        self._parent = parent
        self.img_dir = img_dir
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoNone)

    def canInsertFromMimeData(self, source: QMimeData):
        if source.hasImage():
            return True
        else:
            return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source: QMimeData):
        if source.hasImage():
            image = source.imageData()
            name = f'{time.time()}.png'
            image.save(target_path=Path(self.img_dir) / self._parent.current_aid / f'{time.time()}.png')
            cursor = self.textCursor()
            cursor.insertText(f'![{name}]({name})')
        else:
            return super(MarkdownQTextEdit, self).insertFromMimeData(source)

    def loadResource(self, t, name):
        super().loadResource(t, name)

    def insert_image(self, source_path: Path):
        name = source_path.name
        target_path = Path(self.img_dir) / str(self._parent.current_aid) / name
        shutil.copy(source_path, target_path)
        cursor = self.textCursor()
        cursor.insertText(f'![{name}]({name})')
