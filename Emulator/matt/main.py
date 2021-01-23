from PyQt5 import QtWidgets , QtCore
from MainWindow import MainWindow
import os
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    pass



