from Internal.app_gui_list_builder import *

class FactionChoiceWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FactionChoiceWindow, self).__init__()
        self.ui = None
        loadUi("Internal/faction-choice.ui", self)
        self.faction_list = factions
        self.detachments_list = []
        self.chosen_faction = ""
        self.chosen_detachment = ""
        self.setup_ui(self)
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

    @staticmethod
    def hide_ui(faction_selection_window):
        central_widget = QtWidgets.QWidget(faction_selection_window)
        central_widget.hide()

    def setup_ui(self, faction_selection_window):
        faction_selection_window.setObjectName("FactionChoiceWindow")
        QtCore.QMetaObject.connectSlotsByName(faction_selection_window)

        # Connect signals to the methods.
        self.factionChoiceBox.currentTextChanged.connect(self.faction_changed)
        self.factionChoiceOKButton.clicked.connect(self.pressed_ok)
