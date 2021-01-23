import sys
from PyQt5 import QtWidgets, uic , QtGui

from v4 import Ui_MainWindow
import sys
import os
import re
import json
import csv
import time
import ast
from PyQt5.QtCore import QProcess


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # self.setStyleSheet('background-color:white')
        self.setupUi(self)
        self.logger.setReadOnly(True)

        ##Variablesssssss
        #self.cwd = os.environ["HOME"]
        self.file_path = ""
        self.p = None
        res = {}

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
        if(stdout[0:3]=="000"):
            csvwrite(stdout[3:])
        else:
            self.message(stdout[3:])

    def csvwrite(str):
        #string = "{'datetime': '2005-03-03 21:00:00+00:00', 'portfolio value': 102414.47733204845, 'portfolio pnl': 2414.477332048453, 'portfolio return': 0.02414477332048426, 'portfolio cash': -0.8786679515492573, 'portfolio capital used': -100000.87866795165, 'portfolio positions exposure': 102415.356, 'portfolio positions value': 102415.356, 'number of orders': 25, 'number of open orders': 0, 'number of open positions': 1, 'P': 1.492, 'EV': 0.011839805767318351}"
        #info = json.loads(string) # convert dictionary string to dictionary
        info = ast.literal_eval(str)
        fieldnames = info.keys()
        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            csv_writer.writeheader()

        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            csv_writer.writerow(info)

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


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
