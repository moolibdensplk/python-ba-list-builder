import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from app_main_window import BAAMainMenuWindow
from boarding_actions_list import *

app = QtWidgets.QApplication(sys.argv)
main_window = BAAMainMenuWindow()
main_window.show()

# testing shit
# test_data = load_faction_data("Tau Empire")
# test_units = test_data['Boarding Actions Units']
# print(test_units)
# for unit in test_units.keys():
#    print(unit)

sys.exit(app.exec_())