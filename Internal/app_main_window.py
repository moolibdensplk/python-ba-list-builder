from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Internal.factionChoiceWindow import *
import sys


class BAAMainMenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(BAAMainMenuWindow, self).__init__()
        loadUi("ui/new-window.ui", self)

        def close_pressed():
            sys.exit(1)

        def save_pressed():
            print("SAVE or SaveAs pressed")

        def newPressed():
            self.faction_choice_window = BAAFactionChoiceWindow()
            self.faction_choice_window.show()
            self.hide()

        def open_pressed():
            print("OPEN FILE button or menu pressed")

        # CONNECT the menu objects to functions above
        self.actionNew_menu.triggered.connect(newPressed)
        self.actionOpen_menu.triggered.connect(open_pressed)
        self.actionSave_menu.triggered.connect(save_pressed)
        self.actionSave_As_menu.triggered.connect(save_pressed)
        self.actionExit_menu.triggered.connect(close_pressed)

        #connect buttons to the same functions
        self.new_list_button.clicked.connect(newPressed)
        self.open_list_button.clicked.connect(open_pressed)
        self.close_app_button.clicked.connect(close_pressed)




