from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from Internal.Config import *
from Internal.app_gui_list_builder import *
import sys
import os



class FactionChoiceWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FactionChoiceWindow, self).__init__()
        loadUi("Internal/faction-choice.ui", self)
        self.faction_list = factions
        self.detachments_list = []
        self.chosen_faction = ""
        self.chosen_detachment = ""
        self.setupUi(self)
        self.show()



    def faction_changed(self, selected_faction):
        self.detachmentChoiceBox.clear()
        self.detachments_list = get_detachment_names(selected_faction)
        self.detachmentChoiceBox.addItems(self.detachments_list)

    def pressed_ok(self):
        self.chosen_faction = self.factionChoiceBox.currentText()
        self.chosen_detachment = self.detachmentChoiceBox.currentText()
        if self.chosen_faction in factions:
            self.ui = ListBuilderWindow(self.chosen_faction,self.chosen_detachment)

    def hideUi(self, FactionChoiceWindow):
        self.centralwidget = QtWidgets.QWidget(FactionChoiceWindow)
        self.centralwidget.hide()



    def setupUi(self, FactionChoiceWindow):
        FactionChoiceWindow.setObjectName("FactionChoiceWindow")
        QtCore.QMetaObject.connectSlotsByName(FactionChoiceWindow)

        # Connect signals to the methods.
        self.factionChoiceBox.currentTextChanged.connect(self.faction_changed)
        self.factionChoiceOKButton.clicked.connect(self.pressed_ok)
