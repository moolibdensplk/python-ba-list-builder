from Internal.app_gui_main import *
from PyQt5.QtWidgets import QApplication


def main():
    # create a PyQT5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = BoardingActionsListGuiMain()
    window.show()

    # start the app
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


