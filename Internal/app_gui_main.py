from PyQt5.uic import loadUi
from Internal.app_gui_faction_choice import *
import sys
import os


class BoardingAtctionsListGuiMain(QtWidgets.QMainWindow):
    def __init__(self):
        super(BoardingAtctionsListGuiMain, self).__init__()
        loadUi("Internal/new-window.ui", self)
        self.setupUi(self)

    def new_pressed(self):
        faction_choice_window = QtWidgets.QMainWindow()
        self.ui = FactionChoiceWindow()
        self.ui.setupUi(faction_choice_window)
        faction_choice_window.show()

    def open_pressed(self):
        print("OPEN button or menu pressed")
        home_dir = os.environ['HOME']
        print("DEBUG: home directory: %s" % home_dir)
        fname = QtWidgets.QFileDialog.getOpenFileName()
        print("selected file: "+fname[0])

    def save_pressed(self):
        print("SAVE button or menu pressed")
        home_dir = os.environ['HOME']
        print("DEBUG: home directory: %s" % home_dir)
        fname = QtWidgets.QFileDialog.getSaveFileName()

    def close_pressed(self):
        print("CLOSE button or menu pressed")
        self.close()
        sys.exit(0)

    def setupUi(self, BoardingAtctionsListGuiMain):
        BoardingAtctionsListGuiMain.setObjectName("BoardingAtctionsListGuiMain")
        QtCore.QMetaObject.connectSlotsByName(BoardingAtctionsListGuiMain)
        # connect buttons / menu items to function
        self.actionOpen_menu.triggered.connect(self.open_pressed)
        self.actionSave_menu.triggered.connect(self.save_pressed)
        self.actionSave_As_menu.triggered.connect(self.save_pressed)
        self.actionExit_menu.triggered.connect(self.close_pressed)
        # connect buttons to the same functions
        self.new_list_button.clicked.connect(self.new_pressed)
        self.open_list_button.clicked.connect(self.open_pressed)
        self.close_app_button.clicked.connect(self.close_pressed)
