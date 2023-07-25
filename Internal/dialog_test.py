import sys
from PyQt5 import QtWidgets
from faction_choice_dialog import BAAFactionChoiceDialog

app = QtWidgets.QApplication(sys.argv)
dialog_window = BAAFactionChoiceDialog()

dialog_window.show()

# testing shit
# test_data = load_faction_data("Tau Empire")
# test_units = test_data['Boarding Actions Units']
# print(test_units)
# for unit in test_units.keys():
#    print(unit)

sys.exit(app.exec_())