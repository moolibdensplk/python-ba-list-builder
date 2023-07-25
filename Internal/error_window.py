from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore


class BAAErrorWindow(QtWidgets.QDialog):
    def __init__(self, my_msg, msg_type):
        self.msg_type = msg_type
        self.my_msg = my_msg


        super(BAAErrorWindow, self).__init__()
        loadUi("ui/error-window.ui", self)
        #self.setLayout(QtWidgets.QVBoxLayout())
        if msg_type == "err":
            color_effect_err = QtWidgets.QGraphicsColorizeEffect()
            color_effect_err.setColor(QtCore.Qt.darkRed)
            self.errorLabel.setGraphicsEffect(color_effect_err)
            self.errorLabel.setStyleSheet("font-weight: bold")
        else:
            color_effect_err = QtWidgets.QGraphicsColorizeEffect()
            color_effect_err.setColor(QtCore.Qt.darkGreen)
            self.errorLabel.setGraphicsEffect(color_effect_err)
            self.errorLabel.setStyleSheet("font-weight: bold")

        self.errorLabel.setText(self.my_msg)
        #self.layout().addWidget(self.errorLabel)
        #self.layout().addWidget(self.errorButtonBox)


        """ For some reason this doesn't work with error dialog widget ...
        it keeps complaining that BAAFactionChoiceDialog is not defined ... 
        def go_back():
            print("GOING BACK TO Faction Choice Dialog")
            self.faction_choice_dialog = BAAFactionChoiceDialog()
            self.faction_choice_dialog.show()

        self.errorButtonBox.accepted.connect(go_back)
        """