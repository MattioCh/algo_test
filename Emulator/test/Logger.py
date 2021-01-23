import sys
from PyQt5 import QtWidgets, uic , QtGui

from UiPy.Logger import Ui_Form
import sys 
import os 
import re
from PyQt5.QtCore import QProcess


class Logger(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # self.logger.setReadOnly(True)
        
    
    


