from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from listBuilderWindow import *
from error_window import *
import sys


class BAAFactionChoiceWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(BAAFactionChoiceWindow, self).__init__()
        # self.available_factions = get_factions()
        self.available_factions = get_factions()
        loadUi("ui/faction-choice.ui", self)
        self.factionChoiceBox.setObjectName("factionChoiceBox")
        self.factionChoiceBox.addItems(self.available_factions)


        def faction_selected():
            selected_faction = self.factionChoiceBox.currentText()
            if  selected_faction in self.available_factions:
               # print("Chose faction %s, and pressed NEXT." % selected_faction)
                self.list_builder_window = BAAListBuilderWindow(selected_faction)
                self.list_builder_window.show()
                self.hide()
            else:
                # print("ERROR: you have to choose a faction !")
                error_text = "ERROR: you have to choose a faction !"
                self.error_window = BAAErrorWindow(error_text, "err")
                self.error_window.show()

        self.pushButton.clicked.connect(faction_selected)

