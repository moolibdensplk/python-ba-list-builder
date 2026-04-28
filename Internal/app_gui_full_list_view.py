from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets

class BoardingPatrolViewWindow(QtWidgets.QMainWindow):
    def __init__(self, boarding_patrol_data):
        super(BoardingPatrolViewWindow, self).__init__()
        loadUi("Internal/boarding-patrol-view.ui", self)
        # boarding patrol object stores the full list...
        self.boarding_patrol = boarding_patrol_data
        self.setup_ui(self)
        self.show()

    def close_view_window(self):
        self.close()

    def setup_ui(self, view_window):
        view_window.setObjectName("ListBuilderWindow")
        QtCore.QMetaObject.connectSlotsByName(view_window)

        # format data and display it in the text box (textEdit box)
        # make the box READ ONLY
        self.boardingPatrolTextView.setReadOnly(True)
        self.boardingPatrolTextView.setHtml(self.boarding_patrol)

        # connect / configure button(s)
        # button 1: closeBoardingPatrolViewWindow
        self.closeBoardingPatrolViewWindow.clicked.connect(self.close_view_window)
