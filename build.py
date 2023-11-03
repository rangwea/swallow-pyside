import os
import sys
from pathlib import Path

import nuitka

pkg_path = Path(nuitka.__file__).parent.parent

if sys.platform == "darwin":
    try:
        cmd = f'''
        python -m nuitka --follow-imports --enable-plugin=pyside6 --standalone --macos-create-app-bundle \
            --macos-app-icon=logo.png \
            --nofollow-import-to=objc \
            --nofollow-import-to=numpy \
            --include-data-dir=lib=lib \
            --include-package=markdown.extensions \
            --include-package=pygments.lexers \
            --include-module=pygments.formatters.html \
            --include-module=pygments.styles.default \
            --include-data-dir={pkg_path}/objc=objc \
            --include-data-dir={pkg_path}/PyObjCTools=PyObjCTools \
            --include-module=plistlib \
            --include-package=pkg_resources \
            main.py
        '''
        os.system(cmd)
        print(cmd)
    except Exception as e:
        print(e)
