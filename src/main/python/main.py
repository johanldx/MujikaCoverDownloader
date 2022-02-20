from fbs_runtime.application_context.PySide2 import ApplicationContext

from package.main_window import MainWindow

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = MainWindow()
    window.resize(750, 450)
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)