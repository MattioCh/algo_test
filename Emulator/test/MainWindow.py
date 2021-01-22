import sys
from PyQt5 import QtWidgets, uic , QtGui

from UiPy.v5 import Ui_MainWindow
from Logger import Logger
import sys 
import os 
import re
from PyQt5.QtCore import QProcess


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # self.logger.setReadOnly(True)
        self.Logger = Logger()
        self.Logger.show()

class Logger(QtWidgets.QPlaintText, )

