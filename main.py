import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from Internal.app_main_window import BAAMainMenuWindow
from Internal.boarding_actions_list import *

app = QtWidgets.QApplication(sys.argv)
main_window = BAAMainMenuWindow()
main_window.show()
sys.exit(app.exec_())
