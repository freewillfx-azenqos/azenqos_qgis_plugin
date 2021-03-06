import PyQt5
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog
import os

import azq_utils


class select_log_dialog(QDialog):
    
    # selected_log_singal = pyqtSignal(str)

    def __init__(self, device_configs):
        super(select_log_dialog, self).__init__(None)
        self.logs = device_configs
        self.log = 0
        self.setAttribute(PyQt5.QtCore.Qt.WA_DeleteOnClose)
        self.setupUi()

    def setupUi(self):
        dirname = os.path.dirname(__file__)
        self.ui = loadUi(azq_utils.get_module_fp("select_log_dialog.ui"), self)
        self.setWindowIcon(QIcon(QPixmap(os.path.join(dirname, "icon.png"))))
        self.setWindowTitle("Select Log")
        for n in range(len(self.logs)):
            self.ui.comboBox.addItem(self.logs[n]["name"])
        self.ui.comboBox.currentIndexChanged.connect(self.select_log)

    def select_log(self):
        self.log = self.ui.comboBox.currentIndex()

