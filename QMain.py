from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtWidgets, uic
import sys

from GraphiCrawl import Ui_Form
from acaCrawler import *

class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()