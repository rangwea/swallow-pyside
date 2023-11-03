# -*- coding: utf-8 -*-
import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from swallow.views.window import MainWindow
from swallow.style import STYLE
from swallow.service import Api

app_name = 'swallow'
home_path = Path.home() / f'.{app_name}'
home_path.mkdir(exist_ok=True)

log_file = home_path / 'out.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename=log_file.absolute()
                    )

base_dir = Path(__file__).parent
logging.info(f'base dir:{base_dir}')


if __name__ == '__main__':
    app = QApplication([])
    api = Api(base_dir, home_path)
    win = MainWindow(api)
    win.setStyleSheet(STYLE)
    win.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        api.hugos.close_pre()
