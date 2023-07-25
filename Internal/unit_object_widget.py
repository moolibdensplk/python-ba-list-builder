from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from boarding_actions_list import *
from error_window import *
import sys


class BAAListUnitObjectWidget(QtWidgets.QWidget):
    def __init__(self, unit_data):
        super(BAAListUnitObjectWidget, self).__init__()
        self.unit_data = unit_data
        self.resize(950, 60)
        self.unitWidgetRemoveButton = QtWidgets.QPushButton(self)
        self.unitWidgetRemoveButton.setGeometry(QtCore.QRect(859, 0, 80, 51))
        self.unitDataTableWidget = QtWidgets.QTableWidget(self)
        self.unitDataTableWidget.setGeometry(QtCore.QRect(0, 0, 861, 51))
        self.unitDataTableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.unitDataTableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.unitDataTableWidget.setShowGrid(True)
        self.unitDataTableWidget.setColumnCount(3)
        self.unitDataTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.unitDataTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.unitDataTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.unitDataTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.unitDataTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.unitDataTableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.unitDataTableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.unitDataTableWidget.setItem(0, 2, item)
        self.unitDataTableWidget.horizontalHeader().setVisible(True)
        self.unitDataTableWidget.horizontalHeader().setDefaultSectionSize(255)
        self.unitDataTableWidget.setSortingEnabled(False)
        __sortingEnabled = self.unitDataTableWidget.isSortingEnabled()
        self.unitDataTableWidget.setSortingEnabled(__sortingEnabled)
        self.unitWidgetRemoveButton.setText("REMOVE")
        self.unitDataTableWidget.horizontalHeader().setVisible(True)
        self.unitDataTableWidget.horizontalHeader().setDefaultSectionSize(255)
        item = self.unitDataTableWidget.horizontalHeaderItem(0)
        item.setText("Unit Name")
        item = self.unitDataTableWidget.horizontalHeaderItem(1)
        item.setText("Unit Cost")
        item = self.unitDataTableWidget.horizontalHeaderItem(2)
        item.setText("Unit Dependencies (Required Units)")
        name_item = self.unitDataTableWidget.item(0, 0)
        cost_item = self.unitDataTableWidget.item(0, 1)
        dep_item = self.unitDataTableWidget.item(0, 2)
        name_item.setText(self.unit_data['unit_name'])
        cost_item.setText(str(self.unit_data['unit_cost']))
        dep_item.setText(str(self.unit_data['requires']))
        QtCore.QMetaObject.connectSlotsByName(self)


