from Internal.app_gui_faction_choice import *
import sys

class BoardingActionsListGuiMain(QtWidgets.QMainWindow):
    def __init__(self):
        super(BoardingActionsListGuiMain, self).__init__()
        self.ui = None
        loadUi("Internal/new-window.ui", self)
        self.setup_ui(self)

    def new_pressed(self):
        faction_choice_window = QtWidgets.QMainWindow()
        self.ui = FactionChoiceWindow()
        self.ui.setup_ui(faction_choice_window)
        faction_choice_window.show()

    @staticmethod
    def open_pressed():
        print("[INFO] Feature Currently Not Supported")

    def close_pressed(self):
        self.close()
        sys.exit(0)

    def setup_ui(self, main_window):
        main_window.setObjectName("BoardingActionsListGuiMain")
        QtCore.QMetaObject.connectSlotsByName(main_window)
        # connect buttons / menu items to function
        self.actionOpen_menu.triggered.connect(self.open_pressed)
        self.actionExit_menu.triggered.connect(self.close_pressed)
        # connect buttons to the same functions
        self.new_list_button.clicked.connect(self.new_pressed)
        self.open_list_button.clicked.connect(self.open_pressed)
        self.close_app_button.clicked.connect(self.close_pressed)
