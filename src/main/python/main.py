from fbs_runtime.application_context.PySide2 import ApplicationContext


import sys
from packages.main_window import MainWindow

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(ctx=appctxt)
    window.resize(650, 750)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)