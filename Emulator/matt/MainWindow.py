import sys
from PyQt5 import QtWidgets, uic , QtGui

from v4 import Ui_MainWindow
import sys 
import os 
import re
from PyQt5.QtCore import QProcess
from helper import check_init

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.logger.setReadOnly(True)

        ##Variablesssssss
        self.cwd = os.environ["HOME"]
        self.file_path = ""
        self.p = None


        ## Click functionssssss
        self.find_dir_button.clicked.connect(self.select_file)
        self.start_button.clicked.connect(self.start_backtest)
        self.stop_button.clicked.connect(self.kill_process)
        self.clear_button.clicked.connect(self.clear_log)
        
    
    ##def functionsssss
    def select_file (self):
        dialog = QtWidgets.QFileDialog()
        self.file_path , file_type= dialog.getOpenFileName(None, "Select file",self.cwd,"(*.py)")
        path_string = self.file_path.split("/")
        
        if self.file_path != "":
            self.directory.setText("...  / "+ path_string[-1])

    def message(self, s):
        self.logger.appendPlainText(s)
        pass

    def clear_log(self):
        self.logger.clear()
        pass


    def start_backtest(self):
        if self.p is None:
            self.message("Executing Process")
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)
            # self.p.start("python3", [self.file_path])
            self.p.start("python3", [self.file_path])
        pass

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {   
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def kill_process(self):
        if self.p is not None:
            self.p.kill()
        pass
    
    def process_finished(self):
        self.message("Process finished.")
        self.p = None
        pass
    
    def exitapp(self): 
        sys.exit()


# class Logger(QtWidgets):
#     def __init__(self, parent):      
#         super(Logger, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.setGeometry(QtCore.QRect(20, 390, 451, 151))
#         self.setObjectName("logger")
#     pass


# self.logger = QtWidgets.QPlainTextEdit(self.centralwidget)
#         self.logger.setGeometry(QtCore.QRect(20, 390, 451, 151))
#         self.logger.setObjectName("logger")

