from Internal.app_gui_main import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


def main():
    print("Welcome to super simpel list builder")
    print("WH40k 10th EDITION Boarding Actions")




# Now need to build a basic UI with dropdowns
# select factions
# trying out pyqt 5



    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = BoardingAtctionsListGuiMain()
    window.show()

    # start the app
    sys.exit(app.exec())






if __name__ == '__main__':
    main()


